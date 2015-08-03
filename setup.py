from setuptools import setup, find_packages

setup(
    name="tomorrow",
    version="0.2.3",
    author="Madison May",
    author_email="madison@indico.io",
    packages=find_packages(),
    install_requires=[
        "futures >= 2.2.0"
    ],
    description="""
        Magic decorator syntax for asynchronous code.
    """,
    license="MIT License (See LICENSE)",
    long_description=open("README.rst").read(),
    url="https://github.com/madisonmay/tomorrow"
)
