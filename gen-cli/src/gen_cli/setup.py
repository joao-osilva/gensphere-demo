import click
import os
import json
from .utils import get_config_file

@click.command()
@click.option("-r", "--registry-address", prompt="Enter the registry address (e.g., localhost:5000)", help="The address of the private Docker registry")
def setup(registry_address):
    """Configure the registry address."""
    config_file = get_config_file()
    config_dir = os.path.dirname(config_file)
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        
        config = {"registry_address": registry_address}
        
        with open(config_file, "w") as f:
            json.dump(config, f)
        
        click.echo(f"Registry address set to: {registry_address}")
        click.echo("Setup complete. You can now use other commands.")
    except IOError as e:
        click.echo(f"Error saving configuration: {str(e)}", err=True)
        exit(1)
