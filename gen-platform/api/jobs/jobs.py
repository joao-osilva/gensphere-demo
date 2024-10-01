from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from pymongo import MongoClient
from datetime import datetime, UTC
from bson import ObjectId

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://mongodb:27017/")
db = client["gensphere"]
jobs_collection = db["jobs"]

class JobInput(BaseModel):
    framework: str
    github_url: str
    author: str
    description: str
    expected_inputs: Dict[str, str]
    expected_outputs: Dict[str, str]
    version: str

class Job(JobInput):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

class JobStatusUpdate(BaseModel):
    status: str

@app.post("/create_job")
async def create_job(job: JobInput):
    # Check if the version already exists
    existing_job = jobs_collection.find_one({"github_url": job.github_url, "version": job.version})
    if existing_job:
        raise HTTPException(status_code=400, detail="Version already exists for this GitHub repository")

    # Prepare the job object
    job_dict = job.dict()
    job_dict["status"] = "PENDING"
    job_dict["created_at"] = datetime.now(UTC)
    job_dict["updated_at"] = datetime.now(UTC)

    # Insert the job into MongoDB
    result = jobs_collection.insert_one(job_dict)

    if result.inserted_id:
        return {"message": "Job created successfully", "job_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to create job")

@app.get("/jobs", response_model=List[Job])
async def get_jobs():
    jobs = list(jobs_collection.find())
    for job in jobs:
        job["id"] = str(job["_id"])
        del job["_id"]
    return jobs

@app.put("/jobs/{job_id}/status")
async def update_job_status(job_id: str, status_update: JobStatusUpdate):
    if status_update.status not in ["PENDING", "DONE"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be either PENDING or DONE.")

    try:
        result = jobs_collection.update_one(
            {"_id": ObjectId(job_id)},
            {
                "$set": {
                    "status": status_update.status,
                    "updated_at": datetime.now(UTC)
                }
            }
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"message": "Job status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update job status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)