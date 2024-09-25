from gen_pod_sdk import generate_pod_app
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Define the expected inputs
expected_inputs: Dict[str, Any] = {
    "topic": (str, ...),
    # Add more expected inputs here as needed, e.g.:
    # "max_results": (int, 10),
    # "language": (str, "en"),
}

# Load environment variables from .env file
load_dotenv()

# Get all environment variables
env_vars = dict(os.environ)

# Generate and run the pod app
generate_pod_app(expected_inputs, env_vars)