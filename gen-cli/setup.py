from setuptools import setup, find_packages

setup(
    name="gen-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "gen_cli": ["templates/*"],
    },
    install_requires=[
        "click=>8.1.3",
        "docker=>6.1.3",
        "requests=>2.31.0",
        "pyyaml=>6.0",
    ],
    entry_points={
        "console_scripts": [
            "gen-cli=gen_cli.main:cli",
        ],
    },
    author="Joao Oliveira",
    author_email="joao@gensphere.io",
    description="A CLI tool for interacting with GenSphere platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gen-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.11',
)