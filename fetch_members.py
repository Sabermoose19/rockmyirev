import requests
import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

config = load_config()
ts_id = config.get('ts_id')
api_key = config.get('api_key')

# Replace with your actual ClickUp API token
API_TOKEN = 'pk_88529436_DA8AQ9ELV70YI5HWK9VMQQBIZP5XU06N'
# Replace with your actual ClickUp list ID
LIST_ID = '13769312'

# ClickUp API URL for getting list members
url = f'https://api.clickup.com/api/v2/list/{LIST_ID}/member'

headers = {
    'Authorization': API_TOKEN,
    'Content-Type': 'application/json',
}

print("Connecting to ClickUp...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    members = response.json()
    member_list = []

    for member in members['members']:
        user_id = member['id']
        email = member['email']
        member_list.append({
            'user_id': user_id,
            'email': email
        })
    
    # Save to a local JSON file
    with open('members.json', 'w') as json_file:
        json.dump(member_list, json_file, indent=4)

    print("Successfully connected to ClickUp!")
else:
    print(f"Failed to retrieve members: {response.status_code} - {response.text}")
