from setuptools import setup, find_packages

setup(
    name="gen-pod-sdk",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.115.0",
        "pydantic==2.9.2",
        "crewai==0.63.6",
        "python-dotenv==1.0.1",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A SDK to wrap an AI agent project into a GenSphere pod app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gen-sdk",
)