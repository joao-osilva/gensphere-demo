import os
import click
import docker
import yaml
import requests
from .utils import create_dockerfile
import datetime
import json

@click.command()
@click.option("-p", "--project-path", required=True, type=click.Path(exists=True), help="Path to the FastAPI project")
@click.option("-r", "--repository", required=True, help="Repository name")
@click.option("-i", "--image", required=True, help="Image name")
@click.option("-t", "--tag", required=True, help="Image tag")
@click.pass_context
def build(ctx, project_path, repository, image, tag):
    """
    Build and push a Docker image to the private registry and store agent card in MongoDB.

    This command creates a Dockerfile, builds a Docker image with the specified parameters,
    pushes it to the configured private registry, and stores the agent card in MongoDB.
    """
    registry_address = ctx.obj['registry_address']
    client = docker.from_env(timeout=600)
    
    try:
        # Load agent_card.yml
        agent_card_path = os.path.join(project_path, "agent_card.yml")
        if not os.path.exists(agent_card_path):
            raise click.ClickException("agent_card.yml not found in the project root.")
        
        click.echo("Loading agent_card.yml...")
        with open(agent_card_path, 'r') as f:
            agent_card = yaml.safe_load(f)
        click.echo("agent_card.yml loaded successfully.")
        
        # Create Dockerfile
        dockerfile_path = create_dockerfile(project_path)

        image_tag = f"{registry_address}/{repository}/{image}:{tag}"
        build_date = datetime.datetime.now(datetime.UTC).isoformat()
        
        # Prepare custom labels
        labels = {
            "org.gensphere.img-full-tag": image_tag,
            "org.gensphere.build-date": build_date
        }
        
        # Build image
        click.echo(f"Building image: {image_tag}")
        image, _ = client.images.build(
            path=project_path,
            dockerfile=dockerfile_path,
            tag=image_tag,
            labels=labels,
            nocache=True
        )
        
        # Push image to registry
        click.echo(f"Pushing image: {image_tag}")
        push_output = client.images.push(image_tag, stream=True, decode=True)
        for line in push_output:
            if 'error' in line:
                raise Exception(f"Push error: {line['error']}")
        
        # Store agent card in MongoDB
        api_url = f"http://{registry_address.split(':')[0]}:8000/agent_card"
        
        payload = {
            "image_full_tag": image_tag,
            "agent_card": agent_card.get("agent_card", {}),
            "expected_inputs": agent_card.get("expected_inputs", {}),
            "expected_output": agent_card.get("expected_output", {}),
            "build_date": build_date
        }
        
        click.echo("Preparing to store agent card in MongoDB...")
        click.echo(f"API URL: {api_url}")
        
        response = requests.post(api_url, json=payload)
        click.echo(f"Response content: {response.text}")
        
        response.raise_for_status()
        
        click.echo(f"Image {image_tag} built and pushed successfully")
        click.echo("Agent card stored in MongoDB")        
    except requests.exceptions.RequestException as e:
        click.echo(f"Error storing agent card: {str(e)}", err=True)
        ctx.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        ctx.exit(1)