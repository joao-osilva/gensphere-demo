from gen_pod_sdk import generate_pod_app
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Define the expected inputs
expected_inputs: Dict[str, Any] = {expected_inputs}

# Define the expected output
expected_output: Dict[str, Any] = {expected_outputs}

# Define the node card
node_card: Dict[str, Any] = {
    "author": "{author}",
    "description": "{description}",
    "framework": "{framework}",
    "github_url": "{github_url}",
    "image": "{image_name}"
}

# Load environment variables from .env file
load_dotenv()

# Get all environment variables
env_vars = dict(os.environ)

# Generate and run the pod app
generate_pod_app(expected_inputs, expected_output, node_card, env_vars)
