import logging
from .crewai_wrapper import CrewAIPodWrapper
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn
import os
import yaml

logger = logging.getLogger(__name__)

def generate_pod_app(expected_inputs: Dict[str, Any], expected_output: Dict[str, Any], node_card: Dict[str, Any], env_vars: Dict[str, str] = None):
    """
    Generate and run a GenPod application for a CrewAI project.

    This function sets up the environment, creates a CrewAIPodWrapper,
    generates a GenPod app with the necessary endpoints, and runs the app.

    Args:
        expected_inputs (Dict[str, Any]): A dictionary of expected input types for the crew.
        expected_output (Dict[str, Any]): A dictionary of expected output types from the crew.
        node_card (Dict[str, Any]): A dictionary containing node card information.
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
    
    # Generate node_card.yml file
    generate_node_card_yaml(project_path, expected_inputs, expected_output, node_card)
    logger.info("node_card.yml file generated")

    # Create the wrapper
    wrapper = CrewAIPodWrapper(project_path, expected_inputs, expected_output, node_card)
    logger.info("CrewAIPodWrapper created")
    
    # Generate the FastAPI app
    app = FastAPI()
    wrapper.generate_endpoints(app)
    logger.info("GenPod app generated with endpoints")
    
    # Run the app
    logger.info("Starting the GenPod app")
    uvicorn.run(app, host="0.0.0.0", port=80)

def generate_node_card_yaml(project_path: str, expected_inputs: Dict[str, Any], expected_output: Dict[str, Any], node_card: Dict[str, Any]):
    """
    Generate the node_card.yml file with node card info, expected inputs, and expected outputs.

    Args:
        project_path (str): The path to the project directory.
        expected_inputs (Dict[str, Any]): A dictionary of expected input types.
        expected_output (Dict[str, Any]): A dictionary of expected output types.
        node_card (Dict[str, Any]): A dictionary containing node card information.
    """
    def type_to_str(t):
        return t.__name__ if isinstance(t, type) else str(t)

    node_card_data = {
        "node_card": node_card,
        "expected_inputs": {k: type_to_str(v) for k, v in expected_inputs.items()},
        "expected_output": {k: type_to_str(v) for k, v in expected_output.items()}
    }

    file_path = os.path.join(project_path, "node_card.yml")
    with open(file_path, "w") as yaml_file:
        yaml.dump(node_card_data, yaml_file, default_flow_style=False)

    logger.info(f"node_card.yml file created at {file_path}")