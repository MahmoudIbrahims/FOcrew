import requests

# Beam endpoint URL
url = "https://da42bdd0-b341-43aa-929e-451fa916ab40.app.beam.cloud"

# Authorization token for the endpoint
auth_token = "Uik_.................."

# The data to send to the model
data = {
    "messages": [
        {"role": "system", "content": "you are model for Assistant FOcrew Multi Agents"},
        {"role": "user", "content": "who are you?"}
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
