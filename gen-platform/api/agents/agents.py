import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List
from pymongo import MongoClient
from datetime import datetime, UTC
from bson import ObjectId
import yaml
import gridfs
import json
import io
import zipfile

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agent API",
    description="API for managing AI Agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# MongoDB connection
try:
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["gensphere"]
    agents_collection = db["ai-agents"]
    fs = gridfs.GridFS(db)
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

class AgentInput(BaseModel):
    """
    Represents the input for creating a new agent.
    """
    agent_name: str
    author: str
    description: str
    version: str
    agent_definition: str

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def parse_json(data):
    return json.loads(json.dumps(data, cls=JSONEncoder))

@app.post("/create_agent", response_model=Dict[str, str])
async def create_agent(
    agent_name: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    version: str = Form(...),
    agent_definition: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    Create a new AI agent in the system.

    Args:
        agent_name (str): The name of the agent.
        author (str): The author of the agent.
        description (str): A description of the agent.
        version (str): The version of the agent.
        agent_definition (str): The YAML definition of the agent.
        files (List[UploadFile]): The dependency files for the agent.

    Returns:
        Dict[str, str]: A dictionary containing a success message and the agent ID.

    Raises:
        HTTPException: If the agent already exists or if there's a failure in creating the agent.
    """
    logger.info(f"Attempting to create agent {agent_name} version {version}")
    
    # Check if the agent already exists
    agent_id = f"{agent_name}_{version}"
    existing_agent = agents_collection.find_one({"_id": agent_id})
    if existing_agent:
        logger.warning(f"Agent {agent_name} version {version} already exists")
        raise HTTPException(status_code=400, detail="Agent with this name and version already exists")

    # Validate YAML
    try:
        yaml.safe_load(agent_definition)
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in agent definition: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid YAML in agent definition")

    # Prepare the agent object
    agent_dict = {
        "_id": agent_id,
        "agent_name": agent_name,
        "author": author,
        "description": description,
        "version": version,
        "agent_definition": agent_definition,
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC),
        "dependency_files": []
    }

    # Store dependency files in GridFS
    for file in files:
        file_id = fs.put(file.file, filename=file.filename)
        agent_dict["dependency_files"].append({"filename": file.filename, "file_id": file_id})

    # Insert the agent into MongoDB
    try:
        result = agents_collection.insert_one(agent_dict)
        if result.inserted_id:
            logger.info(f"Agent created successfully with ID: {result.inserted_id}")
            return {"message": "Agent created successfully", "agent_id": str(result.inserted_id)}
        else:
            logger.error("Failed to create agent: No ID returned from MongoDB")
            raise HTTPException(status_code=500, detail="Failed to create agent")
    except Exception as e:
        logger.error(f"Failed to create agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create agent: {str(e)}")

@app.get("/agents", response_model=List[Dict])
async def get_agents():
    """
    Retrieve all agents from the system.

    Returns:
        List[Dict]: A list of all agents in the system.

    Raises:
        HTTPException: If there's a failure in retrieving the agents.
    """
    logger.info("Retrieving all agents")
    try:
        agents = list(agents_collection.find({}, {"agent_definition": 0, "dependency_files": 0}))
        logger.info(f"Retrieved {len(agents)} agents")
        return parse_json(agents)
    except Exception as e:
        logger.error(f"Failed to retrieve agents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve agents: {str(e)}")

@app.get("/agents/{agent_id}", response_model=Dict)
async def get_agent(agent_id: str):
    """
    Retrieve a specific agent from the system.

    Args:
        agent_id (str): The ID of the agent to retrieve.

    Returns:
        Dict: The agent details.

    Raises:
        HTTPException: If the agent is not found or if there's a failure in retrieving the agent.
    """
    logger.info(f"Retrieving agent with ID: {agent_id}")
    try:
        agent = agents_collection.find_one({"_id": agent_id})
        if agent:
            logger.info(f"Retrieved agent: {agent_id}")
            return parse_json(agent)
        else:
            logger.warning(f"Agent not found: {agent_id}")
            raise HTTPException(status_code=404, detail="Agent not found")
    except Exception as e:
        logger.error(f"Failed to retrieve agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve agent: {str(e)}")

@app.get("/agents/{agent_id}/download")
async def download_agent(agent_id: str):
    """
    Download the agent definition and dependency files as a zip file.

    Args:
        agent_id (str): The ID of the agent to download.

    Returns:
        StreamingResponse: A zip file containing the agent definition and dependency files.

    Raises:
        HTTPException: If the agent is not found or if there's a failure in creating the zip file.
    """
    logger.info(f"Preparing download for agent with ID: {agent_id}")
    try:
        agent = agents_collection.find_one({"_id": agent_id})
        if not agent:
            logger.warning(f"Agent not found: {agent_id}")
            raise HTTPException(status_code=404, detail="Agent not found")

        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add agent definition
            zip_file.writestr(f"{agent['agent_name']}_definition.yml", agent['agent_definition'])

            # Add dependency files
            for file_info in agent.get('dependency_files', []):
                file_data = fs.get(file_info['file_id'])
                zip_file.writestr(file_info['filename'], file_data.read())

        # Prepare the response
        zip_buffer.seek(0)
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={agent['agent_name']}_{agent['version']}.zip"
            }
        )

    except Exception as e:
        logger.error(f"Failed to create download for agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create download for agent: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Agent API server")
    uvicorn.run(app, host="0.0.0.0", port=8002)
