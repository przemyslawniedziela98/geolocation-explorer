import logging
from flask import Blueprint, request, jsonify
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
location_bp = Blueprint('location', __name__)

GEOCODE_URL = "https://nominatim.openstreetmap.org/reverse.php"
WIKI_URL = "https://pl.wikipedia.org/api/rest_v1/page/summary/{}"

def get_city_name(lat: float, lon: float) -> str:
    """
    Fetch the city or town name from given latitude and longitude using Nominatim API.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        str: The name of the city or town if found, otherwise 'Nieznana lokalizacja'.
    """
    params = {"lat": lat, "lon": lon, "zoom": 18, "format": "jsonv2"}
    headers = {"User-Agent": "localisation_explorer"}
    
    response = requests.get(GEOCODE_URL, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("address", {}).get("city") or data.get("address", {}).get("town", "Nieznana lokalizacja")
    
    logging.error(f"Failed to fetch city name: {response.status_code} {response.text}")
    return "Nieznana lokalizacja"

def get_wikipedia_summary(city: str) -> dict:
    """
    Fetch a summary of a city from Wikipedia using the Wikipedia API.

    Args:
        city (str): The name of the city to fetch information for.

    Returns:
        dict: A dictionary containing the Wikipedia article title, extract, and URL. If no article is found, returns a default message.
    """
    response = requests.get(WIKI_URL.format(city.replace(" ", "_")))
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data.get("title"),
            "extract": data.get("extract", "Nie znaleziono artykułu."),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page")
        }
    return {"title": city, "extract": "Nie znaleziono artykułu.", "url": None}

@location_bp.route('/get_location', methods=['POST'])
def get_location():
    """
    Handle location data from the client, fetch the city name and Wikipedia summary.

    Returns:
        Response: JSON response containing the city name and Wikipedia summary.
    """
    data = request.json
    lat, lon = data.get("latitude"), data.get("longitude")
    
    if lat is None or lon is None:
        return jsonify({"error": "Invalid coordinates"}), 400
    
    city = get_city_name(lat, lon)
    wiki_info = get_wikipedia_summary(city)
    
    logging.info(f"User located in: {city}")
    return jsonify({"city": city, "wiki": wiki_info})
