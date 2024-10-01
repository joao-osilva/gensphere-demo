from gen_pod_sdk import generate_pod_app
from typing import Dict, Any
import os
import json
from dotenv import load_dotenv

# Define the expected inputs
expected_inputs: Dict[str, Any] = {"topic": "str"}

# Define the expected output
expected_output: Dict[str, Any] = {"result": "str"}

# Define the node card
node_card: Dict[str, Any] = {
    "author": "joao",
    "description": "adslkjnaksjdn",
    "framework": "CrewAI",
    "github_url": "https://github.com/joao-osilva/job_researcher",
    "image": "joao-osilva/job_researcher:1.0"
}

# Load environment variables from .env file
load_dotenv()

# Get all environment variables
env_vars = dict(os.environ)

# Generate and run the pod app
generate_pod_app(expected_inputs, expected_output, node_card, env_vars)