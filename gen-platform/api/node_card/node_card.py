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

app = FastAPI()

# MongoDB connection
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/")
logger.info(f"Connecting to MongoDB at: {mongo_uri}")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["gensphere"]
collection = db["node-card"]

class NodeCard(BaseModel):
    author: str
    description: str
    framework: str
    github_url: str
    image: str

class NodeCardPayload(BaseModel):
    image_full_tag: str
    node_card: NodeCard
    expected_inputs: Dict[str, Any]
    expected_output: Dict[str, Any]
    build_date: str

@app.post("/node_card")
async def create_node_card(payload: NodeCardPayload):
    logger.info(f"Received request to create node card for image: {payload.image_full_tag}")
    try:
        # Convert the Pydantic model to a dictionary
        node_card_dict = payload.dict()
        
        # Use image_tag as the unique identifier
        node_card_dict["_id"] = payload.image_full_tag
        
        logger.debug(f"Storing node card: {json.dumps(node_card_dict, indent=2)}")
        
        # Store node card in MongoDB
        result = collection.replace_one({"_id": payload.image_full_tag}, node_card_dict, upsert=True)
        
        if result.acknowledged:
            logger.info(f"node card stored successfully for image: {payload.image_full_tag}")
            return {"message": "node card stored successfully", "id": payload.image_full_tag}
        else:
            logger.error(f"Failed to store node card for image: {payload.image_full_tag}")
            raise HTTPException(status_code=500, detail="Failed to store node card")
    except Exception as e:
        logger.exception(f"Error storing node card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/node_card/{image_full_tag:path}")
async def get_node_card(image_full_tag: str):
    logger.info(f"Received request to get node card for image: {image_full_tag}")
    try:
        # Decode the URL-encoded image_full_tag
        decoded_image_full_tag = unquote(image_full_tag)
        logger.debug(f"Decoded image_full_tag: {decoded_image_full_tag}")
        
        # Retrieve the node card from MongoDB
        node_card = collection.find_one({"_id": decoded_image_full_tag})
        
        if node_card:
            logger.info(f"node card found for image: {decoded_image_full_tag}")
            # Convert ObjectId to string for JSON serialization
            node_card_json = json.loads(dumps(node_card))
            return node_card_json
        else:
            logger.warning(f"node card not found for image: {decoded_image_full_tag}")
            raise HTTPException(status_code=404, detail=f"node card not found for image_full_tag: {decoded_image_full_tag}")
    except Exception as e:
        logger.exception(f"Error retrieving node card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/node_cards", response_model=List[Dict[str, Any]])
async def get_all_node_cards():
    logger.info("Received request to get all node cards")
    try:
        # Retrieve all node cards from MongoDB
        node_cards = list(collection.find())
        
        if node_cards:
            logger.info(f"Found {len(node_cards)} node cards")
            # Convert ObjectId to string for JSON serialization
            node_cards_json = json.loads(dumps(node_cards))
            return node_cards_json
        else:
            logger.info("No node cards found")
            return []
    except Exception as e:
        logger.exception(f"Error retrieving all node cards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting the API service")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
