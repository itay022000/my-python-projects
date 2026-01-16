Python Starter
==============

A minimal, modern Python project scaffold using `pyproject.toml`.

Getting Started
---------------

1. Create and activate a virtual environment (example using venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2. Install the project in editable mode with dependencies:

```bash
pip install -e .
```

3. Run the app:

```bash
python -m python_starter
```

4. Run tests:

```bash
pytest
```

Project Structure
-----------------

```
python-starter/
  ├─ src/
  │   └─ python_starter/
  │       ├─ __init__.py
  │       └─ __main__.py
  ├─ tests/
  │   └─ test_sanity.py
  ├─ .gitignore
  ├─ LICENSE
  ├─ pyproject.toml
  └─ README.md
```

License
-------

MIT










