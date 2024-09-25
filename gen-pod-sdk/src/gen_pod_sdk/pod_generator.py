from .crewai_wrapper import CrewAIPodWrapper
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv

def generate_pod_app(expected_inputs: Dict[str, Any], env_vars: Dict[str, str] = None):
    # Set the environment variables
    if env_vars:
        for key, value in env_vars.items():
            os.environ[key] = value

    # Get the project path (this should be the directory where api.py is located)
    project_path = os.getcwd()
    
    # Create the wrapper
    wrapper = CrewAIPodWrapper(project_path, expected_inputs)
    
    # Generate the FastAPI app
    app = FastAPI()
    wrapper.generate_endpoint(app)
    
    # Run the app
    uvicorn.run(app, host="0.0.0.0", port=80)
