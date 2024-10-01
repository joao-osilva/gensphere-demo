import logging
from typing import Any, Dict, Type
from fastapi import FastAPI, HTTPException
from pydantic import create_model, BaseModel, Field
import importlib
import os
import sys

logger = logging.getLogger(__name__)

class ExpectedIO(BaseModel):
    name: str
    type: str

class NodeCard(BaseModel):
    author: str
    description: str
    framework: str
    github_url: str
    image: str

class NodeCardWithIO(NodeCard):
    expected_inputs: list[ExpectedIO]
    expected_output: list[ExpectedIO]

class CrewAIPodWrapper:
    """
    A wrapper class for CrewAI projects to be used in GenSphere pods.

    This class handles the loading of CrewAI projects, generates input models,
    and creates FastAPI endpoints for the crew's execution and node card retrieval.
    """

    def __init__(self, project_path: str, expected_inputs: Dict[str, Any], expected_output: Dict[str, Any], node_card: Dict[str, Any]):
        """
        Initialize the CrewAIPodWrapper.

        Args:
            project_path (str): The path to the CrewAI project.
            expected_inputs (Dict[str, Any]): A dictionary of expected input types.
            expected_output (Dict[str, Any]): A dictionary of expected output types.
            node_card (Dict[str, Any]): A dictionary containing node card information.
        """
        self.project_path = project_path
        self.expected_inputs = expected_inputs
        self.expected_output = expected_output
        self.node_card = NodeCard(**node_card)
        self.crew_class = self.load_crew_class()

    def find_project_folder(self):
        """
        Find the project folder within the given project path.

        Returns:
            str: The name of the project folder.

        Raises:
            FileNotFoundError: If no project folder is found.
        """
        # First, check if we're already in the src directory
        if os.path.basename(self.project_path) == 'src':
            project_folders = [f for f in os.listdir(self.project_path) if os.path.isdir(os.path.join(self.project_path, f))]
            if not project_folders:
                raise FileNotFoundError(f"No project folder found in {self.project_path}")
            logger.info(f"Project folder found: {project_folders[0]}")
            return project_folders[0]
        
        # If not, look for a src directory
        src_path = os.path.join(self.project_path, "src")
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"'src' folder not found in {self.project_path}")
        
        project_folders = [f for f in os.listdir(src_path) if os.path.isdir(os.path.join(src_path, f))]
        if not project_folders:
            raise FileNotFoundError(f"No project folder found in {src_path}")
        
        logger.info(f"Project folder found: {project_folders[0]}")
        return project_folders[0]  # Return the first project folder found

    def load_crew_class(self):
        """
        Load the CrewAI class from the project.

        Returns:
            type: The loaded CrewAI class.

        Raises:
            FileNotFoundError: If the project folder is not found.
            AttributeError: If the Crew class is not found in crew.py.
        """
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
            
            logger.info(f"Successfully loaded crew class: {crew_class_name}")
            return crew_class
        except Exception as e:
            logger.error(f"Error loading crew class: {str(e)}")
            raise
        finally:
            # Remove the added path
            sys.path.pop(0)

    def generate_input_model(self):
        """
        Generate a Pydantic model for the expected inputs.

        Returns:
            Type[BaseModel]: A Pydantic model for the crew inputs.
        """
        logger.info("Generating input model")
        fields = {}
        for name, type_hint in self.expected_inputs.items():
            if isinstance(type_hint, str):
                # Convert string type hints to actual types
                if type_hint.lower() == 'str':
                    type_hint = str
                elif type_hint.lower() == 'int':
                    type_hint = int
                elif type_hint.lower() == 'float':
                    type_hint = float
                elif type_hint.lower() == 'bool':
                    type_hint = bool
                else:
                    # Default to Any for unknown types
                    type_hint = Any
            fields[name] = (type_hint, Field(...))
        return create_model("CrewInput", **fields)

    def generate_endpoints(self, app: FastAPI):
        """
        Generate FastAPI endpoints for the crew's execution and node card retrieval.

        Args:
            app (FastAPI): The FastAPI application to add the endpoints to.
        """
        self.generate_execute_endpoint(app)
        self.generate_node_card_endpoint(app)

    def generate_execute_endpoint(self, app: FastAPI):
        """
        Generate a FastAPI endpoint for the crew's execution.

        Args:
            app (FastAPI): The FastAPI application to add the endpoint to.
        """
        InputModel = self.generate_input_model()
        
        output_fields = {}
        for name, type_hint in self.expected_output.items():
            output_fields[name] = (type_hint, Field(...))
        OutputModel = create_model("CrewOutput", **output_fields)

        @app.post("/execute", response_model=OutputModel)
        async def execute_crew(input_data: InputModel):
            """
            Execute the CrewAI project with the given inputs.

            Args:
                input_data (InputModel): The input data for the crew.

            Returns:
                OutputModel: The result of the crew's execution.

            Raises:
                HTTPException: If an error occurs during execution.
            """
            crew_instance = self.crew_class()
            try:
                logger.info("Executing crew with input data")
                result = crew_instance.crew().kickoff(inputs=input_data.dict())
                logger.info("Crew execution completed successfully")
                return OutputModel(**result)
            except Exception as e:
                logger.error(f"Error during crew execution: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        logger.info("GenPod execute endpoint generated successfully")

    def generate_node_card_endpoint(self, app: FastAPI):
        """
        Generate a FastAPI endpoint for retrieving the node card information.

        Args:
            app (FastAPI): The FastAPI application to add the endpoint to.
        """
        @app.get("/node_card", response_model=NodeCardWithIO)
        async def get_node_card():
            """
            Retrieve the node card information.

            Returns:
                NodeCardWithIO: The node card information with expected inputs and outputs.
            """
            def get_type_name(t):
                return t if isinstance(t, str) else (t.__name__ if hasattr(t, '__name__') else str(t))

            expected_inputs = [
                ExpectedIO(name=k, type=get_type_name(v))
                for k, v in self.expected_inputs.items()
            ]
            expected_output = [
                ExpectedIO(name=k, type=get_type_name(v))
                for k, v in self.expected_output.items()
            ]
            return NodeCardWithIO(
                **self.node_card.dict(),
                expected_inputs=expected_inputs,
                expected_output=expected_output
            )

        logger.info("GenPod node_card endpoint generated successfully")