# dotvar: Enhanced Environment Variable Management for Python

A simple Python module to load environment variables from a `.env` file with robust interpolation support.

### The Problems with `python-dotenv`

The De facto `python-dotenv` loads environment variables, but it has two limitations: First, it does not support `auto_load` upon import. Two, **it does not support variable interpolation** within the `.env` file. This means that environment variables cannot reference other variables within the `.env` file, leading to increased potential for errors.

For example, the `CACHE_DIR` variable in the following `.env` file would not automatically resolve to
`$HOME/.cache/myapp`. In fact, your app will create a `$HOME` directory.

```env
CACHE_DIR=$HOME/.cache/myapp
```

In the following example, `python-dotenv` will not resolve `API_ENDPOINT` to `https://api.example.com/v1/`,
requiring manual variable exapantion in your code.

```env
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1/
```

```python
import os

base_url = os.environ.get("BASE_URL")
api_endpoint = os.environ.get("API_ENDPOINT")  # Would be "${BASE_URL}/v1/" instead of the resolved URL
```

## Introducing `dotvar`

`dotvar` addresses the limitations of `python-dotenv` by

1. providing **robust variable interpolation** capabilities. This feature allows environment variables to reference and build upon each other within the `.env` file, promoting DRY (Don't Repeat Yourself) principles and reducing redundancy.
2. provide the optional `dotenv.auto_load` entrypoint, to allow **loading upon import**. Use the `noinspection` and `# noqa` tags to avoid pyCharm from removing the import. (And switch to pyCharm if you are using vscode.)

   ```python
   # noinspection PyUnresolvedReferences
   import dotvar.auto_load  # noqa
   ```

## Installation

```bash
pip install dotvar
```

## Simple Usage

```python
import dotvar

# Load environment variables from the nearest .env file
dotvar.load_env()

# Or specify the path to the .env file
dotvar.load_env(env_path="/path/to/your/.env")
```

## Auto Loading Upon Import

We provide an optional `dotenv.auto_load` entrypoint. Use the `noinspection` and `# noqa` tags to avoid pyCharm from removing the import. (And switch to pyCharm if you are using vscode.)

```python
# noinspection PyUnresolvedReferences
import dotvar.auto_load  # noqa
```


## Interpolated Variables

`dotvar` supports variable interpolation, enabling environment variables to reference other variables within the `.env` file. This feature
enhances flexibility and reduces duplication in configuration files.

### Example `.env` File

```env
# Sample .env file with interpolated variables
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1/
SECRET_KEY=s3cr3t
API_KEY=${SECRET_KEY}_api
```

### Usage in Python

```python
import os
import dotvar

# Load environment variables from the .env file
dotvar.load_env()

base_url = os.environ.get("BASE_URL")
api_endpoint = os.environ.get("API_ENDPOINT")
secret_key = os.environ.get("SECRET_KEY")
api_key = os.environ.get("API_KEY")

print(f"Base URL: {base_url}")
print(f"API Endpoint: {api_endpoint}")
print(f"Secret Key: {secret_key}")
print(f"API Key: {api_key}")
```

### Output

```
Base URL: [https://api.example.com](https://api.example.com)
API Endpoint: [https://api.example.com/v1/](https://api.example.com/v1/)
Secret Key: s3cr3t 
API Key: s3cr3t_api
```

## Differences from `python-dotenv`

While both `dotvar` and `python-dotenv` serve the primary purpose of loading environment variables from a `.env` file, there are key
differences that set `dotvar` apart:

- **Variable Interpolation**: Unlike `python-dotenv`, `dotvar` natively supports variable interpolation, allowing environment variables to
  reference other variables within the `.env` file. This reduces redundancy and enhances readability.
- **Simplicity and Lightweight**: `dotvar` is designed to be lightweight with minimal dependencies, making it ideal for projects that
  require a straightforward solution without the overhead of additional features.
- **Performance**: `dotvar` is optimized for faster loading of environment variables, which can be beneficial in large projects or
  applications where startup time is critical.
- **Error Handling**: `dotvar` includes improved error handling mechanisms to provide clearer feedback when issues arise in the `.env` file,
  such as missing variables or invalid formats.
- **Customization**: `dotvar` allows for greater customization in how environment variables are loaded and managed, offering developers more
  control over the configuration process.

Choosing between `dotvar` and `python-dotenv` depends on the specific needs of your project. If you require a lightweight, performant tool
with robust interpolation and customization options, `dotvar` is the ideal choice. On the other hand, if your project already heavily
integrates with `python-dotenv` and you rely on its specific features, it may be more practical to continue using it.

## Autoload Feature

`dotvar` offers an **autoload** feature that automatically loads environment variables without requiring explicit calls to `load_env()` in
your code. This ensures that environment variables are available as soon as your application starts, simplifying the configuration process.

### Enabling Autoload

To enable the autoload feature, simply import `dotvar` at the beginning of your application's entry point. `dotvar` will automatically
detect and load the `.env` file without any additional function calls.

```python
import dotvar
import os

# Environment variables are automatically loaded
database_url = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("SECRET_KEY")
debug_mode = os.environ.get("DEBUG")
api_key = os.environ.get("API_KEY")

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
print(f"Debug Mode: {debug_mode}")
print(f"API Key: {api_key}")
```

### Testing Autoload

To ensure that the autoload feature is working correctly, you can write tests that verify environment variables are loaded automatically
upon application startup.

#### Example Test Using `pytest`

```python
# tests/test_autoload.py

import os
import pytest
import tempfile

# this automatically loads the env vars
from dotvar import autoload

@pytest.fixture
def temp_env_file_autoload(monkeypatch):
    # Create a temporary .env file
    temp_dir = tempfile.TemporaryDirectory()
    env_path = os.path.join(temp_dir.name, ".env")
    with open(env_path, "w") as f:
        f.write("""
        # Sample .env file with autoload
        DATABASE_URL=postgres://user:password@localhost:5432/dbname
        SECRET_KEY=s3cr3t
        DEBUG=True
        API_KEY=${SECRET_KEY}_api
        """)
    # Mock the path to the .env file
    monkeypatch.setattr(dotvar, 'find_env_path', lambda: env_path)
    # Importing dotvar will trigger autoload
    import dotvar
    yield env_path
    temp_dir.cleanup()


def test_autoload(temp_env_file_autoload):
    database_url = os.environ.get("DATABASE_URL")
    secret_key = os.environ.get("SECRET_KEY")
    debug_mode = os.environ.get("DEBUG")
    api_key = os.environ.get("API_KEY")

    assert database_url == "postgres://user:password@localhost:5432/dbname"
    assert secret_key == "s3cr3t"
    assert debug_mode == "True"
    assert api_key == "s3cr3t_api"
```

#### Running the Test

To run the test, navigate to your project directory and execute:

```bash
pytest tests/test_autoload.py
```

If the autoload feature is functioning correctly, all assertions should pass, confirming that environment variables are loaded
automatically.

## A Detailed Example

```python
import dotvar

# Autoload is enabled by simply importing dotvar
# No need to call load_env()

# Now you can access the variables via os.environ
import os

database_url = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("SECRET_KEY")
debug_mode = os.environ.get("DEBUG")
api_key = os.environ.get("API_KEY")

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
print(f"Debug Mode: {debug_mode}")
print(f"API Key: {api_key}")
```

## To Develop:

### Description of Makefile Targets

- **help**: Displays available Makefile targets.
- **install**: Installs or upgrades the necessary packaging tools (`pip`, `setuptools`, `wheel`, and `twine`).
- **test**: Runs the test suite using `pytest`.
- **build**: Builds the source and wheel distribution packages.
- **clean**: Removes build artifacts to ensure a clean state.
- **upload**: Uploads the built distribution packages to PyPI using `twine`. This target depends on the `build` target.

### Usage

To use the Makefile, open your terminal, navigate to your project directory (where the Makefile is located), and run the desired target. For
example:

- To install dependencies:
  ```bash
  make install
  ```
- To run tests:
  ```bash
  make test
  ```
- To build the package:
  ```bash
  make build
  ```
- To upload the package to PyPI:
  ```bash
  make upload
  ```
- To clean build artifacts:
  ```bash
  make clean
  ```

## License

MIT License
