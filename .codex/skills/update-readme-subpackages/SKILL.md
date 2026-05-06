---
name: update-readme-subpackages
description: Scan the ai_tooling package tree and pyproject.toml to refresh the README package table for repo-local tools. Use when Codex needs to discover ai_tooling subpackages, inspect their code, map Poetry CLI scripts to those subpackages, and update README.md with package descriptions and invocation commands.
---

# Update README Subpackages

Refresh the package overview table in `README.md` from the current source tree instead of preserving stale table rows.

Before editing:

1. Run `scripts/discover_subpackages.py` to collect subpackage names and any matching Poetry scripts.
2. Read `pyproject.toml` to confirm the script mappings and package-data conventions.
3. Read each discovered subpackage's `__init__.py` and any tool-specific modules such as `cli.py` to understand its user-facing purpose.

When updating `README.md`:

1. Keep the package overview as a Markdown table with the columns `Package`, `Description`, and `CLI`.
2. Include one row per user-facing `ai_tooling` subpackage.
3. Write each description as one sentence grounded in the current code, not guessed from the package name alone.
4. Show each CLI invocation as `poetry run <script-name>` when a Poetry script points at that subpackage.
5. Use an empty cell when a subpackage has no CLI script.

After editing, re-read `README.md` and make sure every listed package still exists and every CLI command still matches `pyproject.toml`.

Read [references/checklist.md](references/checklist.md) before substantial README table updates.
