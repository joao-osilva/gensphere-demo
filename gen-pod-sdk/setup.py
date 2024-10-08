from setuptools import setup, find_packages

setup(
    name="gen-pod-sdk",
    version="0.0.1",  # Incremented version number
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi>=0.115.0",
        "pydantic>=2.9.2",
        "crewai>=0.63.6",
        "uvicorn>=0.30.6",
        "pyyaml>=6.0",
    ],
    author="Joao Oliveira",
    author_email="joao@gensphere.io",
    description="A SDK to wrap an AI agent project into a GenSphere pod app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gensphere/gen-pod-sdk",  # Updated URL
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