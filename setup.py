from setuptools import setup, find_packages

setup(
    name="tomorrow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "futures >= 2.2.0"
    ]
)
