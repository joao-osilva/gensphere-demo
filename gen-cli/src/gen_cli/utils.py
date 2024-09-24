import os
import json
import click
import pkg_resources

def create_dockerfile(project_path):
    try:
        # Load Dockerfile template
        dockerfile_template = pkg_resources.resource_string(__name__, 'templates/Dockerfile.template').decode('utf-8')
        
        dockerfile_path = os.path.join(project_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_template)
        
        # Create requirements.txt if it doesn't exist
        requirements_path = os.path.join(project_path, "requirements.txt")
        if not os.path.exists(requirements_path):
            default_requirements = pkg_resources.resource_string(__name__, 'templates/default_requirements.txt').decode('utf-8')
            with open(requirements_path, "w") as f:
                f.write(default_requirements.strip())
        
        return dockerfile_path
    except IOError as e:
        click.echo(f"Error creating Dockerfile: {str(e)}", err=True)
        raise

def get_config_file():
    config_dir = click.get_app_dir("private-registry-cli")
    return os.path.join(config_dir, "config.json")

def is_setup_complete():
    config_file = get_config_file()
    return os.path.exists(config_file)

def get_registry_address():
    config_file = get_config_file()
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
            return config.get("registry_address")
        except json.JSONDecodeError:
            click.echo("Error: Invalid configuration file. Please run 'gen-cli setup' again.", err=True)
            exit(1)
    else:
        click.echo("Registry address not configured. Please run 'gen-cli setup' first.", err=True)
        exit(1)
