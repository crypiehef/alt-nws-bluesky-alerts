import requests
import time
from atproto import Client

# Configuration
VISUAL_CROSSING_API_KEY = "YOUR_VISUAL_CROSSING_API_KEY"
BLUESKY_USERNAME = "YOUR_BLUESKY_USERNAME"
BLUESKY_APP_PASSWORD = "YOUR_BLUESKY_APP_PASSWORD"
LOCATION = "North America"  # Specify the desired location

# Function to get weather alerts
def get_weather_alerts():
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}?key={VISUAL_CROSSING_API_KEY}&alerts=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("alerts", [])
    else:
        print(f"Error fetching alerts: {response.status_code}")
        return []

# Function to post to BlueSky
def post_to_bluesky(message):
    client = Client()
    client.login(BLUESKY_USERNAME, BLUESKY_APP_PASSWORD)
    client.send_post(message)
    print("Posted alert to BlueSky")

# Main logic
def main():
    while True:
        alerts = get_weather_alerts()
        if alerts:
            for alert in alerts:
                if alert.get("severity", "") in ["Severe", "Extreme"]:
                    title = alert.get("event", "Weather Alert")
                    description = alert.get("description", "No details available.")
                    message = f"🚨 {title} 🚨\n{description}"
                    post_to_bluesky(message)
        else:
            print("No new severe weather alerts.")
        
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
