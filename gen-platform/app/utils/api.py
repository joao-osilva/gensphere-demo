import os
import requests
import logging

def get_node_card(image_full_tag):
    """
    Fetch node card information from the API service.
    """
    NODE_CARD_SERVICE_URL = os.environ.get("NODE_CARD_SERVICE_URL", "http://node_card_service:8000")
    try:
        response = requests.get(f"{NODE_CARD_SERVICE_URL}/node_card/{image_full_tag}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching node card: {str(e)}")
        return None