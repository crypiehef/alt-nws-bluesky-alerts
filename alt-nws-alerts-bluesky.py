import requests
import time
from atproto import Client

# Configuration
VISUAL_CROSSING_API_KEY = "RZGVFEAQCWV4DYKJH4FCRQGUW"
BLUESKY_USERNAME = "alt-nws.bsky.social"
BLUESKY_APP_PASSWORD = "zoua-6gdl-jvso-2ozn"
LOCATION = "North America"  # Specify the desired location

# Initialize Bluesky client
client = Client()
client.login(BLUESKY_USERNAME, BLUESKY_APP_PASSWORD)

# Function to get weather alerts and events
def get_weather_data():
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}?key={VISUAL_CROSSING_API_KEY}&alerts=1&include=events"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("alerts", []), data.get("events", [])
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return [], []

# Function to post to BlueSky
def post_to_bluesky(title, description):
    content = f"🚨 {title} 🚨\n{description}"
    client.send_post(text=content)
    print("Posted alert/event to BlueSky")

# Main logic
def main():
    while True:
        alerts, events = get_weather_data()
        
        for alert in alerts:
            severity = alert.get("severity", "")
            if severity in ["Severe", "Extreme"]:
                title = alert.get("event", "Weather Alert")
                description = alert.get("description", "No details available.")
                post_to_bluesky(title, description)
        
        for event in events:
            title = event.get("name", "Weather Event")
            description = event.get("description", "No details available.")
            post_to_bluesky(title, description)
        
        if not alerts and not events:
            print("No new weather alerts or events.")
        
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
