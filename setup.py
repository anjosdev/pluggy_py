from setuptools import setup, find_packages
import os

# Read the README file for the long description.
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pluggy_py",
    version="0.1.0",
    description="Python client for Pluggy API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="anjosdev",
    author_email="viniciusanjosdev@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.32.3,<3.0.0",
        "pydantic>=2.10.6,<3.0.0",
        "setuptools>=75.8.0,<76.0.0",
    ],
)

