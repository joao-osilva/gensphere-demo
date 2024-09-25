from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import create_model
import importlib
import os
import sys

class CrewAIPodWrapper:
    def __init__(self, project_path: str, expected_inputs: Dict[str, Any]):
        self.project_path = project_path
        self.expected_inputs = expected_inputs
        self.crew_class = self.load_crew_class()

    def find_project_folder(self):
        # First, check if we're already in the src directory
        if os.path.basename(self.project_path) == 'src':
            project_folders = [f for f in os.listdir(self.project_path) if os.path.isdir(os.path.join(self.project_path, f))]
            if not project_folders:
                raise FileNotFoundError(f"No project folder found in {self.project_path}")
            return project_folders[0]
        
        # If not, look for a src directory
        src_path = os.path.join(self.project_path, "src")
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"'src' folder not found in {self.project_path}")
        
        project_folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]
        if not project_folders:
            raise FileNotFoundError(f"No project folder found in {src_path}")
        
        return project_folders[0]  # Return the first project folder found

    def load_crew_class(self):
        project_folder = self.find_project_folder()
        
        # If we're already in the src directory, don't add it to the path
        if os.path.basename(self.project_path) == 'src':
            crew_path = os.path.join(self.project_path, project_folder)
        else:
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

    def generate_input_model(self):
        return create_model("CrewInput", **self.expected_inputs)

    def generate_endpoint(self, app: FastAPI):
        InputModel = self.generate_input_model()

        @app.post("/execute")
        async def execute_crew(input_data: InputModel):
            crew_instance = self.crew_class()
            try:
                result = crew_instance.crew().kickoff(inputs=input_data.dict())
                return {"result": result}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
