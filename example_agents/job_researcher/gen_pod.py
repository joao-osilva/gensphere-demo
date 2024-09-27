from gen_pod_sdk import generate_pod_app
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Define the expected inputs
expected_inputs: Dict[str, Any] = {
    "topic": str,
    # Add more expected inputs here as needed, e.g.:
    # "max_results": int,
    # "language": str,
}

# Define the expected output
expected_output: Dict[str, Any] = {
    "research_summary": str,
    "job_opportunities": list,
}

# Define the agent card
agent_card: Dict[str, Any] = {
    "author": "joao",
    "description": "A job researcher agent that provides information on job opportunities based on a given topic.",
    "url": "https://gensphere.io",
    "image": "my-repository/job-researcher",
    "tag": "latest",
}

# Load environment variables from .env file
load_dotenv()

# Get all environment variables
env_vars = dict(os.environ)

# Generate and run the pod app
generate_pod_app(expected_inputs, expected_output, agent_card, env_vars)