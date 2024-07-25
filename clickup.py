import requests

def create_task(api_key, list_id, name, description, priority, assignees):
    # """Creates a task in ClickUp and returns the URL to the newly created task, assigned to specific users."""
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }
    data = {
        'name': name,
        'description': description,
        'priority': priority,
        'assignees': assignees  # This is a list of user IDs
    }
    url = f'https://api.clickup.com/api/v2/list/{list_id}/task'
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        task_id = response.json().get('id')
        task_url = f"https://app.clickup.com/t/{task_id}"
        return task_url
    else:
        print(f"Failed to create task: {response.status_code}, Response: {response.text}")
        return None, None

