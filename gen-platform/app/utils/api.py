import os
import requests
import logging

def get_agent_card(image_full_tag):
    """
    Fetch agent card information from the API service.
    """
    API_SERVICE_URL = os.environ.get("API_SERVICE_URL", "http://api_service:8000")
    try:
        response = requests.get(f"{API_SERVICE_URL}/agent_card/{image_full_tag}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching agent card: {str(e)}")
        return None