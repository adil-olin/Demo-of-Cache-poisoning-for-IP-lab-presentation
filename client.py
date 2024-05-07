import requests
import json

# Define the URL you want to target and the cache key
url = 'http://localhost:8080/some_endpoint?param=value'

# Define the payload to insert into the cache
poisoned_payload = {
    "message": "You have been poisoned!",
    "status": "danger"
}

# Now, send a GET request to see the result
response = requests.get(url)
if response.status_code == 200:
    print("Cached response:", response.json())
else:
    print("Failed to retrieve cached response")
