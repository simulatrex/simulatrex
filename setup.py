from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simulatrex",
    version="0.0.5",
    author="Dominik Scherm",
    author_email="me@dominikscherm.de",
    description="LLM-based simulation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simulatrex/simulatrex",
    packages=find_packages(where="src"),
    include_package_data=True,
    package_dir={"": "src"},
    package_data={
        "simulatrex": ["llm_utils/prompt_templates/*.txt"],
    },
    install_requires=[
        "openai",
        "uuid",
        "pandas",
        "termcolor",
        "chromadb",
        "pydantic",
        "python-dotenv",
        "requests",
        "instructor",
        "SQLAlchemy",
    ],
)
