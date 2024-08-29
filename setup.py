#!/usr/bin/env python3
import setuptools


def get_version() -> str:
    with open("VERSION", "r") as f:
        version = f.read().strip()
    return version


def get_readme() -> str:
    with open("README.md", "r") as fh:
        readme = fh.read()
    return readme


def get_requirements() -> list:
    with open("requirements.txt") as f:
        requirements = f.read().split()
    return requirements


setuptools.setup(
    name="audkenni",
    version=get_version(),
    author="Helgi Hrafn Gunnarsson",
    author_email="helgi@binary.is",
    description="Basic implementation of Auðkenni's REST API for SIM cards.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/binary-is/audkenni",
    packages=setuptools.find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ],
)
