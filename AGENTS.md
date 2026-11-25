# Repository Guidelines

## Project Structure & Module Organization

- `src/` contains Python CloudFormation resource providers. `secrets.py` dispatches Lambda requests to resource-specific modules such as `cfn_secret_provider.py`; `ssm_parameter_name.py` handles parameter naming.
- `tests/` contains pytest suites organized by provider and an AWS resource cleanup script.
- `cloudformation/` holds provider, demo, and CI/CD stack templates.
- `docs/` documents individual custom resources. Update the corresponding document when changing resource properties or outputs.
- `Dockerfile` packages the Lambda container; `Pipfile`, its lockfile, and requirements files define dependencies.

## Build, Test, and Development Commands

Use Python 3.9, as specified by the Pipfile and Lambda image. Make targets require Bash and Unix tools; use a compatible environment such as WSL on Windows.

- `pipenv sync --dev`: install locked runtime and development dependencies.
- `make fmt`: format source and tests with Black; install Black separately if unavailable.
- `make test`: validate every CloudFormation template through AWS, then run pytest with `src/` on `PYTHONPATH`.
- `PYTHONPATH=src pipenv run pytest tests/test_ssm_parameter_name.py`: run a focused suite from Bash.
- `make build`: build the versioned Lambda Docker image; requires Docker and configured AWS CLI credentials for account lookup.

## Coding Style & Naming Conventions

Use four-space indentation and Black formatting. Follow existing `snake_case` module, function, and variable names and `PascalCase` class names. Preserve CloudFormation property names such as `ReturnSecret`. Name provider modules `cfn_<resource>_provider.py`. The legacy `.pep8.rc` specifies a 132-character limit; the formatter target uses Black defaults.

## Testing Guidelines

Name suites `tests/test_*.py` and functions `test_*`. Add regression tests alongside the affected provider, covering request validation and relevant Create, Update, and Delete behavior. No coverage threshold is configured. Many tests call real AWS services and create resources: configure credentials and a region for a dedicated test account. Review the cleanup script before using it; it deletes matching IAM users and SSM parameters.

## Commit & Pull Request Guidelines

History uses `fix:`, `feat:`, and `chore(deps):` prefixes, alongside dependency bump and release messages. Prefer concise, imperative subjects with an appropriate prefix. Pull requests should explain the behavior change, link relevant issues, identify documentation or template changes, and report validation commands and results. Never commit credentials, plaintext secrets, or private keys.
