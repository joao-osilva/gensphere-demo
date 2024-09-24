import click
import requests

@click.command()
@click.pass_context
def list_repositories(ctx):
    """List all repositories in the registry."""
    registry_address = ctx.obj['registry_address']
    base_url = f"http://{registry_address}/v2"
    
    try:
        response = requests.get(f"{base_url}/_catalog")
        response.raise_for_status()
        repositories = response.json().get("repositories", [])
        if repositories:
            click.echo("Repositories:")
            for repo in repositories:
                click.echo(f"- {repo}")
        else:
            click.echo("No repositories found.")
    except requests.RequestException as e:
        click.echo(f"Error fetching repositories: {str(e)}", err=True)
        ctx.exit(1)

@click.command()
@click.option("-r", "--repository", required=True, help="Repository name")
@click.pass_context
def list_tags(ctx, repository):
    """List tags for a specific repository."""
    registry_address = ctx.obj['registry_address']
    base_url = f"http://{registry_address}/v2"
    
    try:
        response = requests.get(f"{base_url}/{repository}/tags/list")
        response.raise_for_status()
        tags = response.json().get("tags", [])
        if tags:
            click.echo(f"Tags for {repository}:")
            for tag in tags:
                click.echo(f"- {tag}")
        else:
            click.echo(f"No tags found for repository '{repository}'.")
    except requests.RequestException as e:
        click.echo(f"Error fetching tags for repository '{repository}': {str(e)}", err=True)
        ctx.exit(1)
