# dotvar: Enhanced Environment Variable Management for Python

A simple Python module to load environment variables from a `.env` file with robust interpolation support.

## Rationale

Managing environment variables is essential for configuring applications without hardcoding sensitive information. Using a `.env` file centralizes configuration parameters, enhancing security and maintainability.

### The Problem with `python-dotenv`

While `python-dotenv` is a popular choice for loading environment variables, it has a notable limitation: **it does not support variable interpolation**. This means that environment variables cannot reference other variables within the `.env` file, leading to redundancies and increased potential for errors. For example:

```env
BASE_URL=https://api.example.com
API_ENDPOINT=${BASE_URL}/v1/
```

In `python-dotenv`, `API_ENDPOINT` would not automatically resolve to `https://api.example.com/v1/`, requiring manual concatenation in your code:

```python
import os

base_url = os.environ.get("BASE_URL")
api_endpoint = os.environ.get("API_ENDPOINT")  # Would be "${BASE_URL}/v1/" instead of the resolved URL
```

This lack of interpolation support can lead to repetitive configurations and make the environment setup less intuitive.

## Introducing `dotvar`

`dotvar` addresses the limitations of `python-dotenv` by providing **robust variable interpolation** capabilities. This feature allows environment variables to reference and build upon each other within the `.env` file, promoting DRY (Don't Repeat Yourself) principles and reducing redundancy.

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

## Interpolated Variables

`dotvar` supports variable interpolation, enabling environment variables to reference other variables within the `.env` file. This feature enhances flexibility and reduces duplication in configuration files.

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