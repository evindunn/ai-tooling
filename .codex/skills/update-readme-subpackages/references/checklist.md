# Checklist

Use this checklist when refreshing the `README.md` package table.

## Discovery

1. Enumerate `ai_tooling` subdirectories that contain `__init__.py`.
2. Ignore helper files at the package root such as `utils.py`.
3. Ignore cache directories and implementation artifacts such as `__pycache__`.

## Reading

1. Read each discovered subpackage's `__init__.py`.
2. Read `cli.py` when present.
3. Read nearby packaged resources only when they materially affect the user-facing description.

## CLI mapping

1. Read `[tool.poetry.scripts]` from `pyproject.toml`.
2. Match script targets to subpackage module paths such as `ai_tooling.<subpackage>.cli:main`.
3. Render CLI commands as `poetry run <script-name>`.

## README output

1. Keep the table columns ordered as `Package`, `Description`, `CLI`.
2. Sort rows by package name unless the repository already uses a different explicit order.
3. Keep descriptions to one sentence.
4. Replace stale rows instead of appending duplicates.
