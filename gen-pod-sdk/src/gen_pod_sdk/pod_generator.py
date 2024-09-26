import logging
from .crewai_wrapper import CrewAIPodWrapper
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn
import os

logger = logging.getLogger(__name__)

def generate_pod_app(expected_inputs: Dict[str, Any], env_vars: Dict[str, str] = None):
    """
    Generate and run a GenPod application for a CrewAI project.

    This function sets up the environment, creates a CrewAIPodWrapper,
    generates a GenPod app with the necessary endpoint, and runs the app.

    Args:
        expected_inputs (Dict[str, Any]): A dictionary of expected input types for the crew.
        env_vars (Dict[str, str], optional): A dictionary of environment variables to set.

    Returns:
        None
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Set the environment variables
    if env_vars:
        for key, value in env_vars.items():
            os.environ[key] = value
        logger.info("Environment variables set")

    # Get the project path (this should be the directory where api.py is located)
    project_path = os.getcwd()
    logger.info(f"Project path: {project_path}")
    
    # Create the wrapper
    wrapper = CrewAIPodWrapper(project_path, expected_inputs)
    logger.info("CrewAIPodWrapper created")
    
    # Generate the FastAPI app
    app = FastAPI()
    wrapper.generate_endpoint(app)
    logger.info("GenPod app generated with endpoint")
    
    # Run the app
    logger.info("Starting the GenPod app")
    uvicorn.run(app, host="0.0.0.0", port=80)
