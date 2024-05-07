import requests
import json

# Define the URL you want to target and the cache key
url = 'http://localhost:8080/some_endpoint?param=value'

# Define the payload to insert into the cache
poisoned_payload = {
    "message": "You have been poisoned!",
    "status": "danger"
}

# Use a PUT request to simulate cache poisoning (real cache poisoning may use other methods)
response = requests.put(url, json=poisoned_payload)
if response.status_code == 200:
    print("Cache poisoned successfully")
