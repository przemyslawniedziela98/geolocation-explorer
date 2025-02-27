# Location Explorer

The Flask app fetches the user's location and provides information about the user's city, such as a Wikipedia summary, fun facts, famous people, and nearby attractions, while also generating an interactive map centered around the provided coordinates. It integrates with APIs like OpenAI for additional insights, OpenStreetMap for geocoding, and Wikipedia.

## Tools Used
- **Flask**
- **Reversed Geocoding**: Utilizes the Nominatim API (from OpenStreetMap) to convert geographical coordinates (latitude and longitude) 
- **OpenAI**: Used for fetching city information using GPT-4o-mini.
- **Folium**: For generating interactive maps that display a location's latitude and longitude.

## Demo
![Gif Explorer](static/gif_geolocation_explorer.gif)
