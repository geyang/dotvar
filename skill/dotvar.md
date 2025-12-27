# dotvar: Environment Variable Loader

Use `dotvar` for loading environment variables from `.env` files with automatic variable interpolation.

## Installation

```bash
pip install dotvar
```

## Usage

### Auto-load (recommended)

Add this import at the top of your entry point:

```python
import dotvar.auto_load  # noqa
```

This automatically loads variables from the nearest `.env` file.

### Strict mode

Use strict mode to raise an error if no `.env` file is found:

```python
import dotvar.auto_load_strict  # noqa
```

### Manual loading

```python
from dotvar import load_env

load_env()  # non-strict (warns if missing)
load_env(strict=True)  # raises if missing
load_env(env_path="/path/to/.env")  # specific path
```

## .env file format

```env
# Comments are supported
DATABASE_URL=postgres://localhost/db
SECRET_KEY=my_secret

# Variable interpolation works
API_ENDPOINT=${DATABASE_URL}/api
FULL_KEY=${SECRET_KEY}_suffix
```

## Key features

- Automatic variable interpolation with `${VAR_NAME}` syntax
- Searches upward from current directory to find `.env`
- No external dependencies (pure Python)
- Supports both quoted and unquoted values
