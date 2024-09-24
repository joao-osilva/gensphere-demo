import os
import requests
import logging
from requests.exceptions import RequestException

class RegistryClientError(Exception):
    """Custom exception for RegistryClient errors"""
    pass

class RegistryClient:
    def __init__(self):
        self.registry_url = os.environ.get("REGISTRY_URL", "http://localhost:5001")
        self.logger = logging.getLogger(__name__)

    def _make_request(self, method, endpoint, **kwargs):
        try:
            response = requests.request(method, f"{self.registry_url}{endpoint}", **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self.logger.error(f"Error making request to {endpoint}: {str(e)}")
            raise RegistryClientError(f"Failed to communicate with registry: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Error parsing JSON response from {endpoint}: {str(e)}")
            raise RegistryClientError(f"Invalid response from registry: {str(e)}")

    def list_repositories(self):
        try:
            data = self._make_request("GET", "/v2/_catalog")
            return data.get("repositories", [])
        except RegistryClientError as e:
            self.logger.error(f"Error listing repositories: {str(e)}")
            raise RegistryClientError("Failed to list repositories") from e

    def list_tags(self, repository):
        try:
            data = self._make_request("GET", f"/v2/{repository}/tags/list")
            return data.get("tags", [])
        except RegistryClientError as e:
            self.logger.error(f"Error listing tags for repository {repository}: {str(e)}")
            raise RegistryClientError(f"Failed to list tags for repository {repository}") from e

    def get_image_details(self, repository, tag):
        try:
            # First, get the manifest
            headers = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}
            manifest = self._make_request("GET", f"/v2/{repository}/manifests/{tag}", headers=headers)
            
            # Extract the config blob digest
            config_digest = manifest['config']['digest']
            
            # Fetch the config blob
            blob = self._make_request("GET", f"/v2/{repository}/blobs/{config_digest}")
            
            # Combine manifest and config information
            details = {
                "manifest": manifest,
                "config": blob
            }
            
            return details
        except RegistryClientError as e:
            self.logger.error(f"Error getting image details for {repository}:{tag}: {str(e)}")
            raise RegistryClientError(f"Failed to get image details for {repository}:{tag}") from e
