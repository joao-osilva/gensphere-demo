FROM python:3.11-slim

WORKDIR /app

# Install git and other necessary build tools
#RUN apt-get update && apt-get install -y git build-essential

# Copy the entire project
COPY . .

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt -v

# Set the entrypoint to run the gen_pod.py file
CMD ["python", "gen_pod.py"]