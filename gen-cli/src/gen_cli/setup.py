import click
import os
import json
from .utils import get_config_file

@click.command()
@click.option("-r", "--registry-address", prompt="Enter the registry address (e.g., localhost:5000)", help="The address of the private Docker registry")
def setup(registry_address):
    """
    Configure the registry address for the gen-cli tool.

    This command sets up the necessary configuration for the gen-cli tool
    by storing the provided registry address in a configuration file.
    """
    config_file = get_config_file()
    config_dir = os.path.dirname(config_file)
    
    click.echo("Starting gen-cli setup...")
    
    try:
        # Ensure the config directory exists
        os.makedirs(config_dir, exist_ok=True)
        click.echo(f"Configuration directory: {config_dir}")
        
        # Prepare the configuration
        config = {"registry_address": registry_address}
        
        # Write the configuration to file
        with open(config_file, "w") as f:
            json.dump(config, f)
        
        click.echo(f"Registry address set to: {registry_address}")
        click.echo(f"Configuration saved to: {config_file}")
        click.echo("Setup complete. You can now use other gen-cli commands.")
    except IOError as e:
        click.echo(f"Error saving configuration: {str(e)}", err=True)
        click.echo("Setup failed. Please try again.", err=True)
        exit(1)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {str(e)}", err=True)
        click.echo("Setup failed. Please try again.", err=True)
        exit(1)
