import os
import requests
from dotenv import load_dotenv

# Resolve path to root folder 
current_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(current_folder)
env_file_path = os.path.join(root_folder, '.env')
load_dotenv(dotenv_path=env_file_path)

class MapsClient:
    """A client to interact with the Google Maps API."""
    
    def __init__(self):
        # Loading API key from env
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coordinates(self, address):
        """Convert a pickup address into latitude and longitude."""

        # Params required by Geocoding API
        params = {
            "address": address,
            "key": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK":
                location = data["results"][0]["geometry"]["location"]
                return location["lat"], location["lng"]
                
            return None, None

        except requests.exceptions.RequestException as e:
            # Catch network errors 
            print(f"Google Maps API error: {e}")
            return None, None