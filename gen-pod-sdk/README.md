# gen-sdk: CrewAI to FastAPI Wrapper

gen-sdk is a Python SDK that allows you to easily wrap your CrewAI projects into FastAPI applications. This tool simplifies the process of exposing your CrewAI crews as API endpoints, making it easier to integrate your AI agents into web applications or microservices.

## Installation

To install gen-sdk, you can use pip:
```bash
pip install gen-sdk
```

## Prerequisites

- Python 3.7+
- A CrewAI project created using the official CLI tool
- OpenAI API key

## Usage

1. First, make sure you have a CrewAI project set up using the CrewAI CLI.

2. In your project directory, create a new file called `api.py` with the following content:

```python
import os
from dotenv import load_dotenv
from gen_sdk import generate_fastapi_app
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

# Generate FastAPI app
app = generate_fastapi_app(project_path, expected_inputs)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

3. Create a `.env` file in the same directory as your `api.py` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

4. Run the FastAPI application:

```bash
python api.py
```

Your CrewAI project is now wrapped in a FastAPI application and running on `http://localhost:8000`.

## API Endpoint

The SDK creates a single endpoint:

- POST `/execute`: Execute the CrewAI project
  - Request body: JSON object with input parameters as defined in `expected_inputs`
  - Response: JSON object with the result of the crew execution

## Example

Assuming you have a CrewAI project that researches a given topic, you can make a POST request to your API like this:

```bash
curl -X POST "http://localhost:8000/execute" -H "Content-Type: application/json" -d '{"topic": "Artificial Intelligence trends"}'
```

## Customizing Inputs

You can customize the inputs your API expects by modifying the `expected_inputs` dictionary in your `api.py` file. For example:

```python
expected_inputs: Dict[str, Any] = {
    "topic": (str, ...),
    "max_results": (int, 10), # Optional input with default value
    "language": (str, "en") # Optional input with default value
}
```

## Error Handling

If the OpenAI API key is not set or if there's an error during the crew execution, the API will return appropriate error messages with a 500 status code.

## Contributing

Contributions to gen-sdk are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.