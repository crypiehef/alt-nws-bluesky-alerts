Simply just uses the Visual Crossing API for weather alerts and when one is available, the script parses it and posts it to BlueSky with custom alert emoji. 

Simply just add your free tier Visual Crossing API key, and your Bluesky account and password in the variables and run. 

The script checks for new alerts every 5 minutes, which is configurable. Be careful with this as the free tier allows you 1000 requests a day.

Python 3 required. 

**Update 0.2 now includes both Alerts and Events. Fires, Tornados and Earthquakes appear under Events while all other weather alerts appear 
under alerts.

**Update 1.0 completely rewritten. Note that you have to enter in the script, the cities you want to monitor for weather alerts.
I started you off with a small list.
