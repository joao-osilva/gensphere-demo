import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from pymongo import MongoClient
from datetime import datetime, UTC
from bson import ObjectId

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Jobs API",
    description="API for managing GenSphere jobs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# MongoDB connection
try:
    client = MongoClient("mongodb://mongodb:27017/")
    db = client["gensphere"]
    jobs_collection = db["jobs"]
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

class JobInput(BaseModel):
    """
    Represents the input for creating a new job.
    """
    framework: str
    github_url: str
    author: str
    description: str
    expected_inputs: Dict[str, str]
    expected_outputs: Dict[str, str]
    version: str

class Job(JobInput):
    """
    Represents a job with additional metadata.
    """
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

class JobStatusUpdate(BaseModel):
    """
    Represents an update to a job's status.
    """
    status: str

@app.post("/create_job", response_model=Dict[str, str])
async def create_job(job: JobInput):
    """
    Create a new job in the system.

    Args:
        job (JobInput): The job details to be created.

    Returns:
        Dict[str, str]: A dictionary containing a success message and the job ID.

    Raises:
        HTTPException: If the version already exists or if there's a failure in creating the job.
    """
    logger.info(f"Attempting to create job for {job.github_url} version {job.version}")
    
    # Check if the version already exists
    existing_job = jobs_collection.find_one({"github_url": job.github_url, "version": job.version})
    if existing_job:
        logger.warning(f"Version {job.version} already exists for {job.github_url}")
        raise HTTPException(status_code=400, detail="Version already exists for this GitHub repository")

    # Prepare the job object
    job_dict = job.dict()
    job_dict["status"] = "PENDING"
    job_dict["created_at"] = datetime.now(UTC)
    job_dict["updated_at"] = datetime.now(UTC)

    # Insert the job into MongoDB
    try:
        result = jobs_collection.insert_one(job_dict)
        if result.inserted_id:
            logger.info(f"Job created successfully with ID: {result.inserted_id}")
            return {"message": "Job created successfully", "job_id": str(result.inserted_id)}
        else:
            logger.error("Failed to create job: No ID returned from MongoDB")
            raise HTTPException(status_code=500, detail="Failed to create job")
    except Exception as e:
        logger.error(f"Failed to create job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")

@app.get("/jobs", response_model=List[Job])
async def get_jobs():
    """
    Retrieve all jobs from the system.

    Returns:
        List[Job]: A list of all jobs in the system.

    Raises:
        HTTPException: If there's a failure in retrieving the jobs.
    """
    logger.info("Retrieving all jobs")
    try:
        jobs = list(jobs_collection.find())
        for job in jobs:
            job["id"] = str(job["_id"])
            del job["_id"]
        logger.info(f"Retrieved {len(jobs)} jobs")
        return jobs
    except Exception as e:
        logger.error(f"Failed to retrieve jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve jobs: {str(e)}")

@app.put("/jobs/{job_id}/status", response_model=Dict[str, str])
async def update_job_status(job_id: str, status_update: JobStatusUpdate):
    """
    Update the status of a specific job.

    Args:
        job_id (str): The ID of the job to update.
        status_update (JobStatusUpdate): The new status for the job.

    Returns:
        Dict[str, str]: A dictionary containing a success message.

    Raises:
        HTTPException: If the status is invalid, the job is not found, or there's a failure in updating the status.
    """
    logger.info(f"Attempting to update status of job {job_id} to {status_update.status}")
    
    if status_update.status not in ["PENDING", "DONE"]:
        logger.warning(f"Invalid status update attempt: {status_update.status}")
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
            logger.warning(f"Job not found: {job_id}")
            raise HTTPException(status_code=404, detail="Job not found")
        logger.info(f"Successfully updated status of job {job_id} to {status_update.status}")
        return {"message": "Job status updated successfully"}
    except Exception as e:
        logger.error(f"Failed to update job status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update job status: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Jobs API server")
    uvicorn.run(app, host="0.0.0.0", port=8001)