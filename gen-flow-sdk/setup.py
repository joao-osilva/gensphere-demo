from setuptools import setup, find_packages

setup(
    name="gen-flow-sdk",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.115.0",
        "pydantic==2.9.2",
        "crewai==0.63.6",
        "uvicorn==0.30.6",
    ],
    author="Daniel Alves",
    author_email="daniel@gensphere.io",
    description="TO-DO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gen-sdk",
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