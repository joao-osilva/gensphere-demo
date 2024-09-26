# Use Python 3.11 slim image as the base
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Streamlit app
CMD ["streamlit", "run", "Home.py"]
