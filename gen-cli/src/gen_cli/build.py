import click
import docker
from .utils import create_dockerfile
import datetime

@click.command()
@click.option("-p", "--project-path", required=True, type=click.Path(exists=True), help="Path to the FastAPI project")
@click.option("-r", "--repository", required=True, help="Repository name")
@click.option("-i", "--image", required=True, help="Image name")
@click.option("-t", "--tag", required=True, help="Image tag")
@click.option("-d", "--description", help="Description of the image")
@click.option("-a", "--author", help="Author of the image")
@click.option("-e", "--email", help="Email of the author")
@click.option("-o", "--organization", help="Organization name")
@click.pass_context
def build(ctx, project_path, repository, image, tag, description, author, email, organization):
    """
    Build and push a Docker image to the private registry.

    This command creates a Dockerfile, builds a Docker image with the specified parameters,
    and pushes it to the configured private registry.
    """
    registry_address = ctx.obj['registry_address']
    client = docker.from_env()
    
    try:
        # Create Dockerfile
        dockerfile_path = create_dockerfile(project_path)
        click.echo(f"Dockerfile created at {dockerfile_path}")
        
        # Prepare custom labels
        labels = {
            "org.gensphere.description": description or "",
            "org.gensphere.author": author or "",
            "org.gensphere.email": email or "",
            "org.gensphere.organization": organization or "",
            "org.gensphere.build-date": datetime.datetime.now(datetime.UTC).isoformat()
        }
        
        # Build image
        image_tag = f"{registry_address}/{repository}/{image}:{tag}"
        click.echo(f"Building image: {image_tag}")
        image, _ = client.images.build(
            path=project_path,
            dockerfile=dockerfile_path,
            tag=image_tag,
            labels=labels,
            nocache=True
        )
        
        # Push image
        click.echo(f"Pushing image: {image_tag}")
        client.images.push(image_tag)
        
        click.echo(f"Image {image_tag} built and pushed successfully")
        click.echo("Custom information added:")
        for key, value in labels.items():
            click.echo(f"  {key}: {value}")
    except docker.errors.BuildError as e:
        click.echo(f"Error building image: {str(e)}", err=True)
        ctx.exit(1)
    except docker.errors.APIError as e:
        click.echo(f"Error pushing image: {str(e)}", err=True)
        ctx.exit(1)