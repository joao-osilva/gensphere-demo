from setuptools import setup, find_packages

setup(
    name="gen-cli",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "gen_cli": ["templates/*"],
    },
    install_requires=[
        "click",
        "docker",
        "requests",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "gen-cli=gen_cli.main:cli",
        ],
    },
)