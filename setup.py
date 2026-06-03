"""
Setup script for Census RAG application.
Helps with easy installation and package distribution.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="census-rag-objectbox",
    version="1.0.0",
    author="Nebeyou Musie",
    author_email="nebeyoumusie@gmail.com",
    description="RAG application using ObjectBox and LangChain for US Census data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshkushwaha7x/census-rag-objectbox",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "census-rag=app.app:main",
        ],
    },
    include_package_data=True,
    keywords="rag langchain objectbox llama3 groq census nlp ai ml",
)
