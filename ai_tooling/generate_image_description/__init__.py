#!/usr/bin/env python3
"""Generate short descriptions for Docker image contexts."""

import functools
import importlib.resources
import json

import openai


@functools.cache
def _load_examples_markdown() -> str:
    """
    Load packaged example descriptions and format them as Markdown.

    :returns: Markdown content for the prompt ``# Examples`` section.
    """
    examples_resource = importlib.resources.files(__package__).joinpath('examples.json')
    examples = json.loads(examples_resource.read_text(encoding='utf-8'))
    if not isinstance(examples, list):
        raise ValueError('Packaged examples must be a JSON array.')

    example_lines: list[str] = []
    for example in examples:
        if not isinstance(example, str):
            raise ValueError('Packaged examples must contain only strings.')
        example_lines.append(f'- {example}')

    return '# Examples\n\n' + '\n'.join(example_lines)


def describe_docker_image(
    client: openai.OpenAI,
    model: str,
    docker_context_summary: str,
) -> dict[str, str]:
    """
    Generate a structured README description response.

    :param client: Configured OpenAI client.
    :param model: Model identifier to call.
    :param docker_context_summary: JSON summary of the Docker context.
    :returns: Mapping returned by the model.
    :raises ValueError: If the model response is empty or invalid JSON.
    """
    response = client.responses.create(
        model=model,
        input=[
            {
                'role': 'developer',
                'content': (
                    'Write a single-sentence README description under 100 characters for the '
                    'Docker image that will be built from the provided Dockerfile '
                    'context. The context is a JSON object where keys are relative '
                    'paths and values are file contents or file metadata. Focus on '
                    'the image purpose, notable bundled software, and runtime role. '
                    'Match the style of the provided README table examples. '
                    'Return a JSON object with exactly one key named "description".'
                ),
            },
            {
                'role': 'user',
                'content': _load_examples_markdown(),
            },
            {
                'role': 'user',
                'content': docker_context_summary,
            },
        ],
        text={
            'format': {
                'type': 'json_schema',
                'name': 'image_description',
                'strict': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'description': {'type': 'string'},
                    },
                    'required': ['description'],
                    'additionalProperties': False,
                },
            },
        },
    )

    if not response.output_text:
        raise ValueError('OpenAI response did not include any text output.')

    parsed_response = json.loads(response.output_text)
    if not isinstance(parsed_response, dict):
        raise ValueError('OpenAI response was not a JSON object.')

    description = parsed_response.get('description')
    if not isinstance(description, str):
        raise ValueError('OpenAI response did not include a string description.')

    return {'description': description}
