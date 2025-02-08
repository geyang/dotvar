import importlib
import os
import sys
import tempfile

import pytest


@pytest.fixture
def temp_env_dir():
    """
    Creates a temporary directory with a .env file for testing.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        env_content = """
        # Sample .env file for autoload testing
        DATABASE_URL=postgres://user:password@localhost:5432/dbname
        SECRET_KEY=s3cr3t
        DEBUG=True
        API_KEY=${SECRET_KEY}_api
        """
        env_path = os.path.join(temp_dir, ".env")
        with open(env_path, "w") as f:
            f.write(env_content)
        yield temp_dir


@pytest.fixture
def clear_env():
    """
    Clears the environment variables that were set during testing.
    """
    for key in ["DATABASE_URL", "SECRET_KEY", "DEBUG", "API_KEY"]:
        os.environ.pop(key, None)


def test_autoload(temp_env_dir, clear_env, monkeypatch):
    """
    Tests that environment variables are automatically loaded when dotvar.auto_load is imported.
    """
    # Step 1: Change the current working directory to the temporary directory
    monkeypatch.chdir(temp_env_dir)

    # Step 2: Ensure that dotvar.auto_load is not already imported
    if 'dotvar.auto_load' in sys.modules:
        del sys.modules['dotvar.auto_load']

    # Step 3: Import dotvar.auto_load and reload it to execute load_env()
    import dotvar.auto_load
    importlib.reload(dotvar.auto_load)

    # Step 4: Assert that the environment variables are loaded correctly
    assert os.environ.get("DATABASE_URL") == "postgres://user:password@localhost:5432/dbname"
    assert os.environ.get("SECRET_KEY") == "s3cr3t"
    assert os.environ.get("DEBUG") == "True"
    assert os.environ.get("API_KEY") == "s3cr3t_api"


def test_autoload_without_env_file(clear_env, monkeypatch):
    """
    Tests that importing dotvar.auto_load without a .env file raises FileNotFoundError
    and does not set any environment variables.
    """
    # Step 1: Create a temporary directory without a .env file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Step 2: Change the current working directory to the temporary directory
        monkeypatch.chdir(temp_dir)

        # Step 3: Ensure that dotvar.auto_load is not already imported
        if 'dotvar.auto_load' in sys.modules:
            del sys.modules['dotvar.auto_load']

        # Step 4: Attempt to import dotvar.auto_load and expect a FileNotFoundError
        with pytest.raises(FileNotFoundError) as exc_info:
            import dotvar.auto_load
            importlib.reload(dotvar.auto_load)

        # Optional: Assert that the exception message is as expected
        assert "No .env file found starting from" in str(exc_info.value)

        # Step 5: Assert that specific environment variables are not set
        assert os.environ.get("DATABASE_URL") is None
        assert os.environ.get("SECRET_KEY") is None
        assert os.environ.get("DEBUG") is None
        assert os.environ.get("API_KEY") is None


