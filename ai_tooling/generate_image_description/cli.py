import argparse
import dataclasses
import json
import pathlib
import sys

import dotenv
import openai

import ai_tooling.utils as utils

from ai_tooling.generate_image_description import generate_image_description


_DEFAULT_MODEL = 'gpt-5-mini'


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate a README description for a Docker image based on its context.',
    )
    parser.add_argument(
        'docker_context',
        type=pathlib.Path,
        help='Path to the Docker context directory.',
    )
    parser.add_argument(
        '--model',
        default=_DEFAULT_MODEL,
        help='OpenAI model to use for description generation.',
    )
    return parser.parse_args()


def _validate_context(context_dir: pathlib.Path) -> None:
    """
    Validate the requested Docker build context.

    :param context_dir: Path to the Docker build context directory.
    :raises ValueError: If the directory or Dockerfile is missing.
    """
    if not context_dir.is_dir():
        raise ValueError(f'{context_dir} is not a valid directory.')

    if not (context_dir / 'Dockerfile').is_file():
        raise ValueError(f'No Dockerfile found in {context_dir}.')


def build_context_mapping(context_dir: pathlib.Path) -> dict[str, object]:
    """
    Build a JSON-serializable mapping for the full Docker context tree.

    :param context_dir: Path to the Docker build context directory.
    :returns: Mapping from relative paths to file or directory data.
    """
    context_mapping: dict[str, object] = {}

    for root_path, dir_names, file_names in utils.iter_directory_entries(context_dir):
        dir_names.sort()
        file_names.sort()

        root_relative = root_path.relative_to(context_dir)
        if root_relative != pathlib.Path('.'):
            context_mapping[root_relative.as_posix()] = {
                'type': 'directory',
                'entries': [*dir_names, *file_names],
            }

        for file_name in file_names:
            file_path = root_path / file_name
            relative_path = file_path.relative_to(context_dir).as_posix()
            context_mapping[relative_path] = dataclasses.asdict(utils.read_file(file_path))

    return context_mapping


def main() -> int:
    """Run the README description generator."""
    dotenv.load_dotenv()

    args = _parse_args()

    try:
        _validate_context(args.docker_context)
        docker_context_mapping = build_context_mapping(args.docker_context)
        docker_context_summary = json.dumps(docker_context_mapping, indent=2, sort_keys=True)
        client = openai.OpenAI()
        description_mapping = generate_image_description(
            client,
            args.model,
            docker_context_summary,
        )
    except (OSError, ValueError, json.JSONDecodeError, openai.OpenAIError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1

    print(json.dumps(description_mapping, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
