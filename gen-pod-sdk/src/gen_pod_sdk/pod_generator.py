from .crewai_wrapper import CrewAIPodWrapper
from typing import Dict, Any

def generate_pod_app(project_path: str, expected_inputs: Dict[str, Any]):
    wrapper = CrewAIPodWrapper(project_path, expected_inputs)
    wrapper.generate_endpoint()
    return wrapper.get_app()
