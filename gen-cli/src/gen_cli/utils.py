import os
import json
import click
import pkg_resources

def create_dockerfile(project_path):
    """
    Create a Dockerfile in the specified project path.

    This function creates a Dockerfile based on a template and also ensures
    that a requirements.txt file exists in the project directory.

    Args:
        project_path (str): The path to the project directory.

    Returns:
        str: The path to the created Dockerfile.

    Raises:
        IOError: If there's an error creating the Dockerfile or requirements.txt.
    """
    try:
        # Load Dockerfile template
        dockerfile_template = pkg_resources.resource_string(__name__, 'templates/Dockerfile.template').decode('utf-8')
        
        dockerfile_path = os.path.join(project_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_template)
        
        click.echo(f"Dockerfile created at {dockerfile_path}")
        
        # Create requirements.txt if it doesn't exist
        requirements_path = os.path.join(project_path, "requirements.txt")
        if not os.path.exists(requirements_path):
            default_requirements = pkg_resources.resource_string(__name__, 'templates/default_requirements.txt').decode('utf-8')
            with open(requirements_path, "w") as f:
                f.write(default_requirements.strip())
            click.echo(f"Default requirements.txt created at {requirements_path}")
        
        return dockerfile_path
    except IOError as e:
        click.echo(f"Error creating Dockerfile: {str(e)}", err=True)
        raise

def get_config_file():
    """
    Get the path to the configuration file.

    Returns:
        str: The path to the configuration file.
    """
    config_dir = click.get_app_dir("gen-cli")
    return os.path.join(config_dir, "config.json")

def is_setup_complete():
    """
    Check if the initial setup has been completed.

    Returns:
        bool: True if setup is complete, False otherwise.
    """
    config_file = get_config_file()
    return os.path.exists(config_file)

def get_registry_address():
    """
    Get the registry address from the configuration file.

    Returns:
        str: The registry address.

    Raises:
        SystemExit: If the configuration file is invalid or not found.
    """
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
