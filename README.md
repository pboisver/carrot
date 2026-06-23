# carrot

Carrot is a small Python package for analyzing animal diet safety relationships from a simple CSV dataset. The repository provides a `DietSafetyManager` utility to answer questions like whether an animal can eat you, whether you can eat it, or whether both are true.

## What this repo contains

- `src/carrot/diet_safety.py`: core business logic for loading `animals.csv` and querying animal relationships.
- `src/carrot/animals.csv`: dataset of animal diet relationships used by the package.
- `example.ipynb`: interactive notebook demonstrating how to load the data and use `DietSafetyManager`.
- `tests/carrot/test_diet_safety.py`: unit tests for the main package API.
- `pyproject.toml`: packaging metadata, dependencies, and install configuration.
- `requirements.txt`: pinned dependency export for environment setup.

> Note: There is also a `src/config_example/` directory in the repository, but it is unrelated to the main `carrot` package and is not covered here.

## Quick start

1. Clone the repository:

```bash
git clone https://github.com/pboisver/carrot.git
cd carrot
```

2. Install `uv` if needed:

```bash
pip install uv
```

3. Install dependencies:

```bash
uv install
```

4. Install the package in editable mode (recommended for development):

```bash
uv pip install -e .
```

> If you only need dependencies for the project, `uv install` is sufficient. Use `uv pip install -e .` afterwards when you want the local package available in editable mode.

4. Use the package from Python:

```python
from carrot.diet_safety import DietSafetyManager

manager = DietSafetyManager(csv_path="src/carrot/animals.csv")
print(manager.get_relationship("Lion"))
print(manager.list_by_category("animal"))
```

## Package API

The primary developer-facing class is `carrot.diet_safety.DietSafetyManager`:

- `DietSafetyManager(csv_path="animals.csv")`
  - Loads the animal dataset from a CSV file.
  - Defaults to `animals.csv` and includes logic for alternate paths in notebook/Colab-style environments.
- `get_relationship(animal_name)`
  - Returns a message describing the relationship for the named animal.
  - Example outputs: `"The animal eats you. Avoid."`, `"You eat the animal. Safe to hunt."`, `"Both: Mutual danger dinner."`, or `"Unknown animal: ..."`.
- `list_by_category(category)`
  - Returns a list of animals for the given category: `"animal"`, `"me"`, or `"both"`.

## Running tests

Run the test suite with `pytest`:

```bash
pytest tests/carrot/test_diet_safety.py
```

## Notebook example

Open `example.ipynb` to see an interactive demonstration of the package. The notebook shows how to import `DietSafetyManager`, load the dataset, query individual animals, and list category-based results.

## Notes for developers

- The package is organized under `src/` and uses `polars` for CSV loading and filtering.
- The actual API surface is the `DietSafetyManager` class; there is no `src/carrot/cli.py` implementation in this repository currently, even though `pyproject.toml` declares a `carrot` script entry point.
- To use the code in a local development environment, make sure `src` is on `PYTHONPATH` or install the package with `pip install -e .`.

## Dependencies

The package requires Python `>=3.12,<4` and depends on:

- `polars`
- `fastapi`
- `typer`
- `uvicorn`
- `pydantic-settings`
- `click`

Dev dependencies are managed in `pyproject.toml` and include `pytest`, `ruff`, `pre-commit`, and `poethepoet`.
