# Development

## Local Environment

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Linting

```bash
ruff check src tests --fix
ruff format src tests
```

## Testing

```bash
python -m pytest
```

## Project Structure

```text
src/
├── capture/
├── detection/
├── storage/
├── dashboard/
└── pipeline.py

tests/
scripts/
docs/
```

## Adding Features

New functionality should be accompanied by:

* Unit tests
* Type annotations
* Documentation updates

External services such as BirdNET, PostgreSQL, and audio devices should be mocked during testing whenever possible.

## CI

The GitHub Actions workflow performs:

* Ruff linting
* Unit testing
* Validation of pull requests

Pull requests should pass all checks before merging into the deployment branch.
