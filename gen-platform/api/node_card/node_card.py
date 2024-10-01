from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from bson.json_util import dumps
import json
import logging
from urllib.parse import unquote

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Node Card API",
    description="API for managing GenSphere node cards",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# MongoDB connection
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/")
logger.info(f"Connecting to MongoDB at: {mongo_uri}")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["gensphere"]
collection = db["node-card"]

class NodeCard(BaseModel):
    """
    Represents a node card with basic information.
    """
    author: str
    description: str
    framework: str
    github_url: str
    image: str

class NodeCardPayload(BaseModel):
    """
    Represents the payload for creating or updating a node card.
    """
    image_full_tag: str
    node_card: NodeCard
    expected_inputs: Dict[str, Any]
    expected_output: Dict[str, Any]
    build_date: str

@app.post("/node_card", response_model=Dict[str, str])
async def create_node_card(payload: NodeCardPayload):
    """
    Create or update a node card in the system.

    Args:
        payload (NodeCardPayload): The node card details to be created or updated.

    Returns:
        Dict[str, str]: A dictionary containing a success message and the node card ID.

    Raises:
        HTTPException: If there's a failure in creating or updating the node card.
    """
    logger.info(f"Received request to create node card for image: {payload.image_full_tag}")
    try:
        node_card_dict = payload.dict()
        node_card_dict["_id"] = payload.image_full_tag
        
        logger.debug(f"Storing node card: {json.dumps(node_card_dict, indent=2)}")
        
        result = collection.replace_one({"_id": payload.image_full_tag}, node_card_dict, upsert=True)
        
        if result.acknowledged:
            logger.info(f"Node card stored successfully for image: {payload.image_full_tag}")
            return {"message": "Node card stored successfully", "id": payload.image_full_tag}
        else:
            logger.error(f"Failed to store node card for image: {payload.image_full_tag}")
            raise HTTPException(status_code=500, detail="Failed to store node card")
    except Exception as e:
        logger.exception(f"Error storing node card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/node_card/{image_full_tag:path}", response_model=Dict[str, Any])
async def get_node_card(image_full_tag: str):
    """
    Retrieve a specific node card from the system.

    Args:
        image_full_tag (str): The full tag of the image associated with the node card.

    Returns:
        Dict[str, Any]: The node card information.

    Raises:
        HTTPException: If the node card is not found or if there's an error retrieving it.
    """
    logger.info(f"Received request to get node card for image: {image_full_tag}")
    try:
        decoded_image_full_tag = unquote(image_full_tag)
        logger.debug(f"Decoded image_full_tag: {decoded_image_full_tag}")
        
        node_card = collection.find_one({"_id": decoded_image_full_tag})
        
        if node_card:
            logger.info(f"Node card found for image: {decoded_image_full_tag}")
            node_card_json = json.loads(dumps(node_card))
            return node_card_json
        else:
            logger.warning(f"Node card not found for image: {decoded_image_full_tag}")
            raise HTTPException(status_code=404, detail=f"Node card not found for image_full_tag: {decoded_image_full_tag}")
    except Exception as e:
        logger.exception(f"Error retrieving node card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/node_cards", response_model=List[Dict[str, Any]])
async def get_all_node_cards():
    """
    Retrieve all node cards from the system.

    Returns:
        List[Dict[str, Any]]: A list of all node cards in the system.

    Raises:
        HTTPException: If there's an error retrieving the node cards.
    """
    logger.info("Received request to get all node cards")
    try:
        node_cards = list(collection.find())
        
        if node_cards:
            logger.info(f"Found {len(node_cards)} node cards")
            node_cards_json = json.loads(dumps(node_cards))
            return node_cards_json
        else:
            logger.info("No node cards found")
            return []
    except Exception as e:
        logger.exception(f"Error retrieving all node cards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting the Node Card API service")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)