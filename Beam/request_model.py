import requests

# Beam endpoint URL
url = "https://eff50fbb-8fcd-4022-9335-030976ce684a.app.beam.cloud"

# Authorization token for the endpoint
auth_token = "Uik_cfGVvVMohAXB6naEpZ0xN0suM5H98ExqYV0QKcOfyY-ccujRkt1ENHMMuFL0phaW8zzu7G1elM-G2szWLA=="

# The data to send to the model
data = {
    "messages": [
        {"role": "system", "content": "you are helpful assastant for code python"},
        {"role": "user", "content": "please create endpint by fastapi"}
    ]
}

# Headers including Authorization
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {auth_token}"
}

# Send POST request
response = requests.post(url, json=data, headers=headers)

# Print the model response
print(response.json())
