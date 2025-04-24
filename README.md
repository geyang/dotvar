# dotvar: Enhanced Environment Variable Management for Python

A simple Python module to load environment variables from a `.env` file with robust interpolation support.

## The Problems with `python-dotenv`

The De facto `python-dotenv` loads environment variables, but it has two limitations: First, it does not support `auto_load` upon import. Two, **it does not support variable interpolation** within the `.env` file. This means that environment variables cannot reference other variables within the `.env` file, leading to increased potential for errors.

For example, the `CACHE_DIR` variable in the following `.env` file would not automatically resolve to
`$HOME/.cache/myapp`. In fact, your app will create a `$HOME` directory.

```env
CACHE_DIR=$HOME/.cache/myapp
```

In the following example, `python-dotenv` will not resolve `API_ENDPOINT` to `https://api.example.com/v1/`,
requiring manual variable expansion in your code.

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

`dotvar` addresses the limitations of `python-dotenv` by:

1. Providing **robust variable interpolation** capabilities. This feature allows environment variables to reference and build upon each other within the `.env` file, promoting DRY (Don't Repeat Yourself) principles and reducing redundancy.
2. Providing the optional `dotvar.auto_load` entrypoint, to allow **loading upon import**. Use the `noinspection` and `# noqa` tags to avoid PyCharm from removing the import.

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

# Use strict mode to raise an error if .env file is not found
dotvar.load_env(strict=True)
```

## Auto Loading Upon Import

We provide an optional `dotvar.auto_load` entrypoint. Use the `noinspection` and `# noqa` tags to avoid PyCharm from removing the import.

```python
# noinspection PyUnresolvedReferences
import dotvar.auto_load  # noqa
```

For strict mode (raises an error if no .env file is found):

```python
# noinspection PyUnresolvedReferences
import dotvar.auto_load_strict  # noqa
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
Base URL: https://api.example.com
API Endpoint: https://api.example.com/v1/
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

## Detailed Examples

### Basic Auto-loading 

```python
# Auto-load is enabled by simply importing the module
import dotvar.auto_load

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

### Testing Examples

```python
# tests/test_auto_load.py

import os
import sys
import tempfile
import pytest

def test_auto_load_with_env_file(monkeypatch):
    """
    Tests that environment variables are automatically loaded when dotvar.auto_load is imported.
    """
    # Create a temporary directory with a .env file
    with tempfile.TemporaryDirectory() as temp_dir:
        env_content = """
        DATABASE_URL=postgres://user:password@localhost:5432/dbname
        SECRET_KEY=s3cr3t
        DEBUG=True
        API_KEY=${SECRET_KEY}_api
        """
        env_path = os.path.join(temp_dir, ".env")
        with open(env_path, "w") as f:
            f.write(env_content)
            
        # Change directory to the temp dir
        monkeypatch.chdir(temp_dir)
        
        # Import the auto_load module
        if 'dotvar.auto_load' in sys.modules:
            del sys.modules['dotvar.auto_load']
            
        import dotvar.auto_load
        
        # Verify the environment variables
        assert os.environ.get("DATABASE_URL") == "postgres://user:password@localhost:5432/dbname"
        assert os.environ.get("SECRET_KEY") == "s3cr3t"
        assert os.environ.get("DEBUG") == "True"
        assert os.environ.get("API_KEY") == "s3cr3t_api"
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging. Here's how to set up a development environment:

1. Install Poetry if you don't have it already:
   ```bash
   pip install poetry
   ```

2. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/geyang/dotvar.git
   cd dotvar
   poetry install
   ```

3. Run tests:
   ```bash
   # Run tests
   poetry run pytest
   
   # Run tests with verbose output
   poetry run pytest -v
   
   # Run tests with coverage report
   poetry run pytest --cov=dotvar --cov-report=term-missing
   ```

4. Build the package:
   ```bash
   poetry build
   ```

5. Publish to PyPI (for maintainers):
   ```bash
   poetry publish --build
   ```

## License

MIT License
