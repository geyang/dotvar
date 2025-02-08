# setup.py

from pathlib import Path

from setuptools import setup, find_packages

# Read the version number from the VERSION file
VERSION = Path(__file__).parent / "VERSION"
with open(VERSION, "r") as version_file:
    version = version_file.read().strip()

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dotvar",  # Updated package name
    version=version,
    author="Ge Yang",  # Updated author name
    author_email="ge.ike.yang@gmail.com",  # Updated author email
    description="A simple module to load environment variables from a .env file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geyang/dot-env",  # Replace with your actual repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)