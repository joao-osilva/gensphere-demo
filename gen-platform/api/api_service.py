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
collection = db["agent-card"]

class AgentCard(BaseModel):
    author: str
    description: str
    image: str
    tag: str
    url: str

class AgentCardPayload(BaseModel):
    image_full_tag: str
    agent_card: AgentCard
    expected_inputs: Dict[str, Any]
    expected_output: Dict[str, Any]
    build_date: str

@app.post("/agent_card")
async def create_agent_card(payload: AgentCardPayload):
    logger.info(f"Received request to create agent card for image: {payload.image_full_tag}")
    try:
        # Convert the Pydantic model to a dictionary
        agent_card_dict = payload.dict()
        
        # Use image_tag as the unique identifier
        agent_card_dict["_id"] = payload.image_full_tag
        
        logger.debug(f"Storing agent card: {json.dumps(agent_card_dict, indent=2)}")
        
        # Store agent card in MongoDB
        result = collection.replace_one({"_id": payload.image_full_tag}, agent_card_dict, upsert=True)
        
        if result.acknowledged:
            logger.info(f"Agent card stored successfully for image: {payload.image_full_tag}")
            return {"message": "Agent card stored successfully", "id": payload.image_full_tag}
        else:
            logger.error(f"Failed to store agent card for image: {payload.image_full_tag}")
            raise HTTPException(status_code=500, detail="Failed to store agent card")
    except Exception as e:
        logger.exception(f"Error storing agent card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent_card/{image_full_tag:path}")
async def get_agent_card(image_full_tag: str):
    logger.info(f"Received request to get agent card for image: {image_full_tag}")
    try:
        # Decode the URL-encoded image_full_tag
        decoded_image_full_tag = unquote(image_full_tag)
        logger.debug(f"Decoded image_full_tag: {decoded_image_full_tag}")
        
        # Retrieve the agent card from MongoDB
        agent_card = collection.find_one({"_id": decoded_image_full_tag})
        
        if agent_card:
            logger.info(f"Agent card found for image: {decoded_image_full_tag}")
            # Convert ObjectId to string for JSON serialization
            agent_card_json = json.loads(dumps(agent_card))
            return agent_card_json
        else:
            logger.warning(f"Agent card not found for image: {decoded_image_full_tag}")
            raise HTTPException(status_code=404, detail=f"Agent card not found for image_full_tag: {decoded_image_full_tag}")
    except Exception as e:
        logger.exception(f"Error retrieving agent card: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent_cards", response_model=List[Dict[str, Any]])
async def get_all_agent_cards():
    logger.info("Received request to get all agent cards")
    try:
        # Retrieve all agent cards from MongoDB
        agent_cards = list(collection.find())
        
        if agent_cards:
            logger.info(f"Found {len(agent_cards)} agent cards")
            # Convert ObjectId to string for JSON serialization
            agent_cards_json = json.loads(dumps(agent_cards))
            return agent_cards_json
        else:
            logger.info("No agent cards found")
            return []
    except Exception as e:
        logger.exception(f"Error retrieving all agent cards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info("Starting the API service")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
