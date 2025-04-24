# dotvar: Smarter Environment Variable Management for Python

`dotvar` is a Python module that improves upon traditional `.env` loaders by providing **automatic loading** and **native variable interpolation**, solving the major shortcomings of `python-dotenv`.

---

## The Problems with `python-dotenv`

While `python-dotenv` is widely used, it has two significant limitations:

1. It **does not support automatic loading** upon import.
2. It **lacks variable interpolation**, so environment variables cannot reference other variables within the same `.env` file.

For example, the following will not be correctly resolved using `python-dotenv`:

```env
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1/
```

```python
import os
print(os.environ.get("API_ENDPOINT"))  # Returns "${BASE_URL}/v1/" instead of the resolved value
```

---

## Introducing `dotvar`

`dotvar` solves these issues by:

- Supporting **native variable interpolation** with `${VAR_NAME}` syntax.
- Offering an **auto-load entrypoint**: just import `dotvar.auto_load`.
- Providing a **strict mode** (`dotvar.auto_load_strict`) that raises an error if `.env` is not found.

---

## Installation

```bash
pip install dotvar  # supports Python 3.7+
```

---

## Usage

Place a `.env` file in your project root:

```env
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1/
API_KEY=s3cr3t_api
```

Then in your Python code:

```python
# noinspection PyUnresolvedReferences
import dotvar.auto_load  # noqa

import os

print(os.environ["BASE_URL"])       # https://api.example.com
print(os.environ["API_ENDPOINT"])   # https://api.example.com/v1/
print(os.environ["API_KEY"])        # s3cr3t_api
```

To use strict mode:

```python
import dotvar.auto_load_strict  # noqa
```

---

## Differences from `python-dotenv`

- ✅ **Built-in Interpolation**: Reference other variables within `.env`.
- ✅ **Auto-load**: Load on import with no extra calls.
- ✅ **Strict Mode**: Catch missing files early in development.
- ✅ **No Dependencies**: Pure Python, standard library only.
- ✅ **Lightweight & Fast**: Minimal footprint, optimized load time.

---

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management.

```bash
# Set up environment
poetry install

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=dotvar --cov-report=term-missing
```

---

## License

MIT License
