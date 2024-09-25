import os
from dotenv import load_dotenv
from gen_sdk import generate_pod_app
import uvicorn
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

# Get the project path
project_path = os.path.dirname(os.path.abspath(__file__))

# Define the expected inputs
expected_inputs: Dict[str, Any] = {
    "topic": (str, ...),
    # Add more expected inputs here as needed, e.g.:
    # "max_results": (int, 10),
    # "language": (str, "en"),
}

# Generate pod app
app = generate_pod_app(project_path, expected_inputs)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)