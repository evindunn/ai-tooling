# AI Tooling

| Package | Description | CLI |
| --- | --- | --- |
| `ai_tooling.generate_image_description` | Generates a short, structured README description for a Docker image by summarizing its build context and querying the OpenAI Responses API. | `poetry run generate-image-description` |

## Repo Skills

### `update-readme-subpackages`

Refreshes the `README.md` package table by scanning `ai_tooling`, reading discovered subpackages, and matching Poetry CLI scripts from `pyproject.toml`.

Invoke it by asking Codex to use [`$update-readme-subpackages`](./.codex/skills/update-readme-subpackages/SKILL.md), for example: `Use $update-readme-subpackages to refresh the README package table.`

## Release Workflow

GitHub Actions publishes releases from Git tags that match `v*`.

- Build locally with `poetry build` if you want to sanity-check artifacts before tagging.
- Push a version tag such as `v0.0.1` to trigger [`.github/workflows/publish.yml`](./.github/workflows/publish.yml).
- The workflow builds the wheel and sdist, attaches them to a GitHub Release, and publishes them to PyPI.
