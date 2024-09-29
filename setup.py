from setuptools import setup, find_packages

setup(
    name="afk_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "parsedatetime",
    ],
    description="A parser for AFK durations",
    author="Imran Khan",
    url="https://github.com/astr0n0mer/afk_parser",
)
