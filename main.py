import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_task(task_id):
    # Retrieve API credentials from environment variables
    user_id = os.getenv("USER_ID")
    api_token = os.getenv("API_TOKEN")

    # Check if the environment variables are available
    if not user_id or not api_token:
        raise ValueError("Missing USER_ID or API_TOKEN in environment variables.")

    # Set up headers for authentication
    headers = {
        "x-api-user": user_id,
        "x-api-key": api_token,
    }

    # Construct the request URL
    base_url = "https://habitica.com/api/v3/tasks"
    request_url = f"{base_url}/{task_id}"

    try:
        # Make a GET request to retrieve the task
        response = requests.get(request_url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response
            task_data = response.json()
            # Check if the task is completed
            if task_data.get("success") and task_data["data"].get("completed"):
                return True
            else:
                return False
        else:
            # Handle different error responses
            response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

    return False

if __name__ == "__main__":
    # Define the task ID you want to retrieve
    task_id = "ec6d9500-4ff8-41d8-b62b-c8c3f90a854a"

    # Call the function and print the result
    is_task_checked_off = get_task(task_id)
    if is_task_checked_off:
        print("The task is checked off.")
    else:
        print("The task is not checked off.")
