import os
import requests
from dotenv import load_dotenv

#load env variables from the .env file
load_dotenv()

# Google Maps API key stored securely in the .env file
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_coordinates(address):
    """
    Convert a pickup address into latitude and longitude
    using the Google Maps Geocoding API.

    Args:
        address (str): The pickup address entered by the business.

    Returns:
        tuple:
            (latitude, longitude) if the address is found,
            otherwise (None, None).
    """

    url = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if data["status"] == "OK":

            location = data["results"][0]["geometry"]["location"]

            latitude = location["lat"]
            longitude = location["lng"]

            return latitude, longitude

        return None, None

    except requests.exceptions.RequestException as e:
        print(f"Google Maps API error: {e}")
        return None, None