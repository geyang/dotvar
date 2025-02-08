# dotvar, a Python module to load environment variables from a `.env` file

A simple Python module to load environment variables from a `.env` file.

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

## A Detailed Example

```python
import dotvar

# Load environment variables from the nearest .env file
dotvar.load_env()

# Now you can access the variables via os.environ
import os

database_url = os.environ.get("DATABASE_URL")
secret_key = os.environ.get("SECRET_KEY")
debug_mode = os.environ.get("DEBUG")

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
print(f"Debug Mode: {debug_mode}")
```

## To Develop:

### Description of Makefile Targets
- **help**: Displays available Makefile targets.
- **install**: Installs or upgrades the necessary packaging tools (`pip`, `setuptools`, `wheel`, and `twine`).
- **test**: Runs the test suite using `unittest`.
- **build**: Builds the source and wheel distribution packages.
- **clean**: Removes build artifacts to ensure a clean state.
- **upload**: Uploads the built distribution packages to PyPI using `twine`. This target depends on the `build` target.

### Usage

To use the Makefile, open your terminal, navigate to your project directory (where the Makefile is located), and run the desired target. For example:

- To install dependencies:
    ``` bash
    make install
    ```
- To run tests:
    ``` bash
    make test
    ```
- To build the package:
    ``` bash
    make build
    ```
- To upload the package to PyPI:
    ``` bash
    make upload
    ```
- To clean build artifacts:
    ``` bash
    make clean
    ```

## License

MIT License
