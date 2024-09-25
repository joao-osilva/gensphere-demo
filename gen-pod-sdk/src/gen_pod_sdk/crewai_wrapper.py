from typing import Any, Dict
from fastapi import FastAPI
from pydantic import create_model
import importlib
import os
import sys

class CrewAIPodWrapper:
    def __init__(self, project_path: str, expected_inputs: Dict[str, Any]):
        self.project_path = project_path
        self.expected_inputs = expected_inputs
        self.app = FastAPI()
        self.crew_class = self.load_crew_class()
        self.crew_instance = None

    def find_project_folder(self):
        src_path = os.path.join(self.project_path, "src")
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"'src' folder not found in {self.project_path}")
        
        project_folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]
        if not project_folders:
            raise FileNotFoundError(f"No project folder found in {src_path}")
        
        return project_folders[0]  # Return the first project folder found

    def load_crew_class(self):
        project_folder = self.find_project_folder()
        crew_path = os.path.join(self.project_path, "src", project_folder)
        
        # Add the project path to sys.path
        sys.path.insert(0, os.path.dirname(crew_path))
        
        try:
            crew_module = importlib.import_module(f"{project_folder}.crew")
            
            # Generate the crew class name
            crew_class_name = ''.join(word.capitalize() for word in project_folder.split('_')) + 'Crew'
            crew_class = getattr(crew_module, crew_class_name, None)
            
            if crew_class is None:
                raise AttributeError(f"Crew class '{crew_class_name}' not found in crew.py")
            
            return crew_class
        finally:
            # Remove the added path
            sys.path.pop(0)

    def initialize_crew(self, inputs=None):
        if inputs is None:
            inputs = {}
        self.crew_instance = self.crew_class()
        return self.crew_instance.crew()

    def generate_input_model(self):
        return create_model("CrewInput", **self.expected_inputs)

    def generate_endpoint(self):
        InputModel = self.generate_input_model()

        @self.app.post("/execute")
        async def execute_crew(input_data: InputModel):
            crew = self.initialize_crew()
            result = crew.kickoff(inputs=input_data.dict())
            return result

    def get_app(self):
        return self.app
