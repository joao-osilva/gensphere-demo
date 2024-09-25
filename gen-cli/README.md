# GenSphere Platform CLI

This CLI tool helps to interact with the GenSphere Platform by providing commands to setup, build, list repositories and tags, and deploy images for AI agents.

## Installation

1. Navigate to the `gen-cli` folder:
```bash
cd gen-cli
```

2. Install the CLI tool:
```bash
pip install -e .
```

## Usage

The CLI provides the following main commands:

### Setup

Configure the registry address:
```bash
gen-cli setup
```
You will be prompted to enter the registry address (e.g., localhost:5000).

### Build

Build and push a Docker image to the private registry:
```bash
gen-cli build --project-path /path/to/fastapi/project --repository myrepo --image myimage --tag latest
```

#### Note on requirements.txt

When building a Docker image, the CLI expects a `requirements.txt` file in your project directory. If one doesn't exist, a basic `requirements.txt` file will be created with FastAPI and Uvicorn as dependencies. If your project requires additional dependencies, make sure to include them in your project's `requirements.txt` file before running the build command.

### List Repositories

List all repositories in the registry:
```bash
gen-cli list-repositories
```

### List Tags

List tags for a specific repository:
```bash
gen-cli list-tags --repository myrepo
```

### Deploy

Deploy a container locally based on existing repo images:
```bash
gen-cli deploy --repository myrepo --image myimage --tag latest --port 8000 --name mycontainer
```

The `deploy` command now requires the following options:
- `--repository` or `-r`: Repository name
- `--image` or `-i`: Image name
- `--tag` or `-t`: Image tag
- `--port` or `-p`: Port to expose
- `--name` or `-n`: Custom name for the container

## Error Handling

The CLI now includes improved error handling. If an error occurs during any operation, you will see a descriptive error message, and the CLI will exit with a non-zero status code.

## Help

For more information on each command, use the `--help` option:
```bash
gen-cli --help
gen-cli setup --help
gen-cli build --help
gen-cli list-repositories --help
gen-cli list-tags --help
gen-cli deploy --help
```

Note: Make sure to run the `setup` command before using other commands to configure the registry address.