import requests
import json
from atproto import Client
from datetime import datetime
import time

# Configuration
API_KEY = "YOUR_VISUAL_CROSSING_API_KEY"  # Replace with your Visual Crossing API key
BLUESKY_USERNAME = "yourusername.bsky.social"  # Replace with your Bluesky username
BLUESKY_PASSWORD = "your-bluesky-password"  # Replace with your Bluesky password
CHECK_INTERVAL = 3600  # Check every hour (3600 seconds)

# List of major US cities to check (you can expand this list)
LOCATIONS = [
    "New York, NY",
    "Los Angeles, CA",
    "Chicago, IL",
    "Houston, TX",
    "Phoenix, AZ",
    "Philadelphia, PA",
    "San Antonio, TX",
    "San Diego, CA",
    "Dallas, TX",
    "Seattle, WA"
]

def get_weather_alerts(location):
    """Fetch weather alerts for a given location from Visual Crossing API."""
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    query = f"{base_url}{location}?unitGroup=us&key={API_KEY}&contentType=json&include=alerts"
    
    try:
        response = requests.get(query)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if "alerts" in data and data["alerts"]:
            return data["alerts"]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {location}: {e}")
        return None

def format_alert_message(alert, location):
    """Format the weather alert into a Bluesky-friendly message."""
    title = alert.get("title", "Weather Alert")
    description = alert.get("description", "No description available")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")
    
    message = (
        f"Weather Alert for {location} ({timestamp}):\n"
        f"{title}\n"
        f"{description[:200]}..."  # Truncate to fit Bluesky's 300-character limit
    )
    return message[:300]  # Ensure it fits within Bluesky's character limit

def post_to_bluesky(message):
    """Post a message to Bluesky."""
    try:
        client = Client()
        client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)
        client.send_post(text=message)
        print(f"Posted to Bluesky: {message}")
    except Exception as e:
        print(f"Error posting to Bluesky: {e}")

def main():
    print("Starting weather alert monitoring...")
    
    while True:
        for location in LOCATIONS:
            alerts = get_weather_alerts(location)
            if alerts:
                for alert in alerts:
                    message = format_alert_message(alert, location)
                    post_to_bluesky(message)
            else:
                print(f"No alerts for {location} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S EST')}")
        
        print(f"Waiting {CHECK_INTERVAL // 60} minutes until next check...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Install required packages if not already installed:
    # pip install requests atproto
    
    main()