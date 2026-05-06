#!/usr/bin/env python3
"""Discover ai_tooling subpackages and associated Poetry scripts."""

import json
import pathlib


def _load_tomllib():
    """
    Load a TOML reader module.

    :returns: Module that provides ``load`` for TOML files.
    :raises ModuleNotFoundError: If neither ``tomllib`` nor ``tomli`` is available.
    """
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    return tomllib


def _discover_subpackages(package_root: pathlib.Path) -> list[str]:
    """
    Discover user-facing ai_tooling subpackages.

    :param package_root: Path to the ``ai_tooling`` package directory.
    :returns: Sorted list of subpackage names.
    """
    subpackages: list[str] = []

    for child_path in sorted(package_root.iterdir()):
        if not child_path.is_dir():
            continue
        if child_path.name.startswith('__'):
            continue
        if not (child_path / '__init__.py').is_file():
            continue
        subpackages.append(child_path.name)

    return subpackages


def _load_poetry_scripts(pyproject_path: pathlib.Path) -> dict[str, str]:
    """
    Load Poetry console-script mappings from ``pyproject.toml``.

    :param pyproject_path: Path to the project's ``pyproject.toml`` file.
    :returns: Mapping of script names to their target entrypoints.
    """
    tomllib = _load_tomllib()
    with pyproject_path.open('rb') as file:
        pyproject_data = tomllib.load(file)

    tool_table = pyproject_data.get('tool', {})
    if not isinstance(tool_table, dict):
        return {}

    poetry_table = tool_table.get('poetry', {})
    if not isinstance(poetry_table, dict):
        return {}

    scripts_table = poetry_table.get('scripts', {})
    if not isinstance(scripts_table, dict):
        return {}

    return {
        script_name: script_target
        for script_name, script_target in scripts_table.items()
        if isinstance(script_name, str) and isinstance(script_target, str)
    }


def _match_scripts_to_subpackage(subpackage_name: str, poetry_scripts: dict[str, str]) -> list[str]:
    """
    Collect Poetry scripts that target a specific subpackage.

    :param subpackage_name: ai_tooling subpackage name.
    :param poetry_scripts: Mapping of Poetry script names to entrypoint targets.
    :returns: Sorted list of matching script names.
    """
    module_prefix = f'ai_tooling.{subpackage_name}.'

    matching_scripts = [
        script_name
        for script_name, script_target in poetry_scripts.items()
        if script_target.startswith(module_prefix)
    ]
    matching_scripts.sort()
    return matching_scripts


def main() -> int:
    """Print discovered subpackages and their CLI scripts as JSON."""
    repo_root = pathlib.Path.cwd()
    package_root = repo_root / 'ai_tooling'
    pyproject_path = repo_root / 'pyproject.toml'

    subpackages = _discover_subpackages(package_root)
    poetry_scripts = _load_poetry_scripts(pyproject_path)

    report = []
    for subpackage_name in subpackages:
        report.append(
            {
                'package': f'ai_tooling.{subpackage_name}',
                'path': f'ai_tooling/{subpackage_name}',
                'scripts': _match_scripts_to_subpackage(subpackage_name, poetry_scripts),
            },
        )

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
