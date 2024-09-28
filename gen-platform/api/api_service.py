from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Dict, Any
import os

app = FastAPI()

# MongoDB connection
mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://mongodb:27017/"))
db = mongo_client["gensphere"]
collection = db["agent-card"]

class AgentCard(BaseModel):
    author: str
    description: str
    image: str
    tag: str
    url: str

class AgentCardPayload(BaseModel):
    image_tag: str
    agent_card: AgentCard
    expected_inputs: Dict[str, Any]
    expected_output: Dict[str, Any]

@app.post("/agent_card")
async def agent_card(payload: AgentCardPayload):
    try:
        # Convert the Pydantic model to a dictionary
        agent_card_dict = payload.dict()
        
        # Use image_tag as the unique identifier
        agent_card_dict["_id"] = payload.image_tag
        
        # Store agent card in MongoDB
        result = collection.replace_one({"_id": payload.image_tag}, agent_card_dict, upsert=True)
        
        if result.acknowledged:
            return {"message": "Agent card stored successfully", "id": payload.image_tag}
        else:
            raise HTTPException(status_code=500, detail="Failed to store agent card")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
