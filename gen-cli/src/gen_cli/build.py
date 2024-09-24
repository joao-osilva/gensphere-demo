import os
import click
import docker
from .utils import create_dockerfile

@click.command()
@click.option("-p", "--project-path", required=True, type=click.Path(exists=True), help="Path to the FastAPI project")
@click.option("-r", "--repository", required=True, help="Repository name")
@click.option("-i", "--image", required=True, help="Image name")
@click.option("-t", "--tag", required=True, help="Image tag")
@click.pass_context
def build(ctx, project_path, repository, image, tag):
    """Build and push a Docker image to the private registry."""
    registry_address = ctx.obj['registry_address']
    client = docker.from_env()
    
    try:
        # Create Dockerfile
        dockerfile_path = create_dockerfile(project_path)
        
        # Build image
        image_tag = f"{registry_address}/{repository}/{image}:{tag}"
        click.echo(f"Building image: {image_tag}")
        image, _ = client.images.build(path=project_path, dockerfile=dockerfile_path, tag=image_tag)
        
        # Push image
        click.echo(f"Pushing image: {image_tag}")
        client.images.push(image_tag)
        
        click.echo(f"Image {image_tag} built and pushed successfully")
    except docker.errors.BuildError as e:
        click.echo(f"Error building image: {str(e)}", err=True)
        ctx.exit(1)
    except docker.errors.APIError as e:
        click.echo(f"Error pushing image: {str(e)}", err=True)
        ctx.exit(1)