import os
import shutil
import time
import git
import docker
import requests
import yaml
import logging
import json
from pymongo import MongoClient
from datetime import datetime, UTC
from bson.objectid import ObjectId
from urllib.parse import urlparse
from string import Template
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MongoDB connection
try:
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["gensphere"]
    jobs_collection = db["jobs"]
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Docker client
try:
    docker_client = docker.from_env(timeout=600)
    logger.info("Successfully initialized Docker client")
except Exception as e:
    logger.error(f"Failed to initialize Docker client: {str(e)}")
    raise

# Registry address
REGISTRY_ADDRESS = "host.docker.internal:5001"

def parse_github_url(url):
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    parts = path.split('/')
    if len(parts) >= 2:
        return parts[0], parts[1]
    else:
        raise ValueError(f"Invalid GitHub URL: {url}")

def create_dockerfile(project_path):
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'Dockerfile.template')
        with open(template_path, 'r') as f:
            dockerfile_content = f.read()
        
        dockerfile_path = os.path.join(project_path, "Dockerfile")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        
        logger.info(f"Dockerfile created at {dockerfile_path}")
        return dockerfile_path
    except Exception as e:
        logger.error(f"Failed to create Dockerfile: {str(e)}")
        raise

def create_gen_pod_file(job, repo_path):
    try:
        git_user, git_repo_name = parse_github_url(job['github_url'])
        image_name = f"{git_user}/{git_repo_name}:{job['version']}"
        
        # Read the template file
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'gen_pod_template.py')
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Create a template object
        template = Template(template_content)
        
        # Substitute the placeholders with actual values
        gen_pod_content = template.safe_substitute(
            expected_inputs=job['expected_inputs'],
            expected_outputs=job['expected_outputs'],
            author=job['author'],
            description=job['description'],
            framework=job['framework'],
            github_url=job['github_url'],
            image_name=image_name
        )
        
        gen_pod_path = os.path.join(repo_path, "gen_pod.py")
        with open(gen_pod_path, "w") as f:
            f.write(gen_pod_content)
        
        logger.info(f"gen_pod.py created at {gen_pod_path}")
    except Exception as e:
        logger.error(f"Failed to create gen_pod.py: {str(e)}")
        raise

def update_job_status(job_id, status):
    try:
        payload = {"status": status}
        response = requests.put(f"http://jobs_service:8001/jobs/{job_id}/status", json=payload)
        response.raise_for_status()
        logger.info(f"Job {job_id} status updated to {status}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update job status for job {job_id}: {str(e)}")

def process_job(job):
    job_id = str(job['_id'])
    logger.info(f"Processing job {job_id}")
    try:
        # Set up the repository path
        repo_path = f"/tmp/{job_id}"
        
        # Clean up existing directory if it exists
        if os.path.exists(repo_path):
            logger.info(f"Cleaning up existing directory: {repo_path}")
            shutil.rmtree(repo_path)
        
        # Clone the repository
        logger.info(f"Cloning repository to {repo_path}")
        git.Repo.clone_from(job['github_url'], repo_path)
        logger.info(f"Repository cloned successfully")

        # Create gen_pod.py file
        create_gen_pod_file(job, repo_path)

        # Create Dockerfile
        dockerfile_path = create_dockerfile(repo_path)

        # Build and push Docker image
        git_user, git_repo_name = parse_github_url(job['github_url'])
        image_name = f"{git_user}/{git_repo_name}:{job['version']}"
        image_tag = f"{REGISTRY_ADDRESS}/{image_name}"
        
        # Prepare custom labels
        build_date = datetime.now(UTC).isoformat()
        labels = {
            "org.gensphere.img-full-tag": image_tag,
            "org.gensphere.build-date": build_date
        }
        
        logger.info(f"Building Docker image: {image_tag}")
        try:
            image, build_logs = docker_client.images.build(
                path=repo_path,
                dockerfile=dockerfile_path,
                tag=image_tag,
                labels=labels,
                nocache=True
            )
            for log in build_logs:
                if 'stream' in log:
                    logger.info(f"Build log: {log['stream'].strip()}")
        except docker.errors.BuildError as e:
            logger.error(f"Docker build error: {str(e)}")
            raise
        
        logger.info(f"Pushing Docker image: {image_tag}")
        try:
            push_logs = docker_client.images.push(image_tag, stream=True, decode=True)
            for log in push_logs:
                if 'status' in log:
                    logger.info(f"Push status: {log['status']}")
                if 'error' in log:
                    raise Exception(f"Push error: {log['error']}")
        except docker.errors.APIError as e:
            logger.error(f"Docker push error: {str(e)}")
            raise

        # Prepare node card payload using job information
        payload = {
            "image_full_tag": image_tag,
            "node_card": {
                "author": job['author'],
                "description": job['description'],
                "framework": job['framework'],
                "github_url": job['github_url'],
                "image": image_name
            },
            "expected_inputs": job['expected_inputs'],
            "expected_output": job['expected_outputs'],
            "build_date": build_date
        }

        logger.info("Storing node card in MongoDB")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        response = requests.post(f"http://node_card_service:8000/node_card", json=payload)
        logger.info(f"Node card storage response: {response.status_code} - {response.text}")
        response.raise_for_status()

        # Update job status to DONE
        update_job_status(job_id, "DONE")
        logger.info(f"Job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}")
        # Job remains in PENDING state, will be retried later

def main():
    while True:
        pending_jobs = jobs_collection.find({"status": "PENDING"})
        for job in pending_jobs:
            process_job(job)
        time.sleep(300)  # Wait for 5min before checking for new jobs

if __name__ == "__main__":
    main()