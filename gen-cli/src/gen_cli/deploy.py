import click
import docker

@click.command()
@click.option("-r", "--repository", required=True, help="Repository name")
@click.option("-i", "--image", required=True, help="Image name")
@click.option("-t", "--tag", required=True, help="Image tag")
@click.option("-p", "--port", required=True, type=int, help="Port to expose")
@click.option("-n", "--name", required=True, help="Custom name for the container")
@click.pass_context
def deploy(ctx, repository, image, tag, port, name):
    """Deploy a container locally based on existing repo images."""
    registry_address = ctx.obj['registry_address']
    client = docker.from_env()
    
    image_tag = f"{registry_address}/{repository}/{image}:{tag}"
    
    try:
        click.echo(f"Pulling image: {image_tag}")
        client.images.pull(image_tag)
        
        click.echo(f"Running container: {image_tag}")
        container = client.containers.run(
            image_tag,
            detach=True,
            ports={f"80/tcp": port},
            name=name
        )
        
        click.echo(f"Container {container.name} is running on port {port}")
    except docker.errors.ImageNotFound:
        click.echo(f"Error: Image {image_tag} not found", err=True)
        ctx.exit(1)
    except docker.errors.APIError as e:
        click.echo(f"Error deploying container: {str(e)}", err=True)
        ctx.exit(1)
