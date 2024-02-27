# Databricks notebook source
import os
from runpy import run_path

from setuptools import find_packages, setup

# read the program version from version.py (without loading the module)
__version__ = run_path('src/ml_devops_dida_task/version.py')['__version__']


def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ml-devops-dida-task",
    version=__version__,
    author="Dr. Jahed Naghipoor",
    author_email="jahednaghipoor1361@gmail.com",
    description="In this project, we deploy a simple text classification service based on a pre-trained NLP",
    license="proprietary",
    url="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'ml_devops_dida_task': ['res/*']},
    long_description=read('README.md'),
    install_requires=[],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pre-commit',
    ],
    platforms='any',
    python_requires='>=3.8',
)
