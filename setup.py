from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simulatrex",
    version="0.0.3.0",
    author="Dominik Scherm",
    author_email="me@dominikscherm.de",
    description="LLM-based simulation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simulatrex/simulatrex",
    packages=find_packages(where="package"),
    include_package_data=True,
    package_dir={"": "package"},
    package_data={
        "simulatrex": ["llm_utils/prompt_templates/*.txt"],
    },
    install_requires=[
        "openai",
        "uuid",
        "numpy",
        "termcolor",
        "chromadb",
        "pydantic",
        "python-dotenv",
        "requests",
        "instructor",
        "SQLAlchemy",
    ],
)
