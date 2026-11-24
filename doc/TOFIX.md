# TOFIX

Findings from a code scan on 2026-10-04.

## Medium

- `tera.snippets/exercises.md.tera:1` - dead snippet: `tera.templates/README.md.tera:40` only includes `tera.snippets/main.md.tera`, so the "Exercises" section (the count of `exercises/*/exercise.md`) never reaches `README.md`. This is the only repo in the fleet with a snippet of that name; rename it to `main.md.tera` and rebuild.
- `pyproject.toml:9` - `pyclassifiers` is a runtime dependency but nothing in the repo imports or uses it (`git grep -i classif` hits only `pyproject.toml` and `uv.lock`). Remove it and refresh `uv.lock`.
- `pyproject.toml:30` - `[[tool.mypy.overrides]]` sets `ignore_missing_imports` for `boto3.*` although `boto3-stubs` is already in the dev group (line 14); the config-level suppression just hides whatever the stubs would catch. Drop the override and fix what mypy then reports.

## Low

- `pyproject.toml:25` - `mypy_path = "src:python:scripts"`, but this repo has none of those directories; remove the setting or point it at `exercises`.
- `exercises/04_lambda/main.tf:23` - provider constraints `~> 5.0` (aws) and `~> 2.0` (archive, line 27) carry no comment saying why; the AWS provider is on 6.x, and `.terraform.lock.hcl` is the place for pinning. Drop the constraints or add a comment explaining them.
