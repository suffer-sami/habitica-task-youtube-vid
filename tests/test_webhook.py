import pytest
from app.server import create_app
from app.config import Config
from app.webhook import process_task_completion

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    Config.SEND_WHATSAPP_MESSAGES = False
    with app.test_client() as client:
        yield client

def test_webhook_no_action(client):
    data = {
        "type": "scored",
        "webhookType": "taskActivity",
        "task": {
            "type": "daily",
            "text": "Wrong Task"
        },
        "direction": "up"
    }
    response = client.post('/webhook', json=data)
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "No action required"}

def test_webhook_process_task(client, mocker):
    mock_process = mocker.patch('app.webhook.process_task_completion')
    mock_process.return_value = {"success": True, "message": "Task completion processed"}
    
    data = {
        "type": "scored",
        "webhookType": "taskActivity",
        "task": {
            "type": "daily",
            "text": Config.TASK_TO_BE_COMPLETED
        },
        "direction": "up"
    }
    response = client.post('/webhook', json=data)
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "Task completion processed"}
    mock_process.assert_called_once()

def test_webhook_invalid_data(client):
    response = client.post('/webhook', data=None, content_type='application/json')
    assert response.status_code == 400
    assert response.json['success'] == False

def test_webhook_missing_data(client):
    response = client.post('/webhook', json={})
    assert response.status_code == 400
    assert response.json["success"] == False

def test_process_task_completion(mocker):
    mock_get_video = mocker.patch('app.webhook.get_latest_video')
    mock_get_video.return_value = "Test URL"
    
    result = process_task_completion()
    assert result == {"success": True, "message": "Task completion processed"}
    mock_get_video.assert_called_once()

def test_webhook_exception(client, mocker):
    mocker.patch('app.webhook.process_task_completion', side_effect=Exception("Test error"))
    
    data = {
        "type": "scored",
        "webhookType": "taskActivity",
        "task": {
            "type": "daily",
            "text": Config.TASK_TO_BE_COMPLETED
        },
        "direction": "up"
    }
    response = client.post('/webhook', json=data)
    assert response.status_code == 500
    assert response.json == {"success": False, "message": "Internal server error"}

def test_webhook_with_whatsapp_enabled(client, mocker):
    Config.SEND_WHATSAPP_MESSAGES = True
    mock_get_video = mocker.patch('app.webhook.get_latest_video')
    mock_get_video.return_value = "Test URL"
    mock_send_whatsapp = mocker.patch('app.webhook.send_whatsapp_message')
    mock_send_whatsapp.return_value = "message_id_123"

    data = {
        "type": "scored",
        "webhookType": "taskActivity",
        "task": {
            "type": "daily",
            "text": Config.TASK_TO_BE_COMPLETED
        },
        "direction": "up"
    }
    response = client.post('/webhook', json=data)
    assert response.status_code == 200
    assert response.json == {"success": True, "message": "Task completion processed"}
    mock_get_video.assert_called_once()
    mock_send_whatsapp.assert_called_once_with("🎁: Test URL")

# import pytest
# import json
# from unittest.mock import patch
# from app.server import create_app
# from app.config import Config
# from app.webhook import process_task_completion

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
    
#     # Ensure SEND_WHATSAPP_MESSAGES is False
#     Config.SEND_WHATSAPP_MESSAGES = False
    
#     with app.test_client() as client:
#         yield client

# def test_webhook(client):
#     # Mock data for the test
#     data = {
#         "type": "scored",
#         "webhookType": "taskActivity",
#         "task": {
#             "type": "daily",
#             "text": "Example Task"
#         },
#         "direction": "up"
#     }

#     # Test with incorrect task name
#     response = client.post('/webhook', data=json.dumps(data), content_type='application/json')
#     assert response.status_code == 200
#     assert response.json['success'] == True
#     assert response.json['message'] == "No action required"

#     # Test with correct task name
#     data['task']['text'] = Config.TASK_TO_BE_COMPLETED
#     with patch('app.webhook.process_task_completion') as mock_process:
#         mock_process.return_value = {"success": True, "message": "Task completion processed"}
#         response = client.post('/webhook', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 200
#         assert response.json['success'] == True
#         assert response.json['message'] == "Task completion processed"
#         mock_process.assert_called_once()

# def test_webhook_invalid_data(client):
#     # Send a request without JSON data
#     response = client.post('/webhook', data=None, content_type='application/json')
#     assert response.status_code == 400
#     assert response.json['success'] == False

# @patch('app.webhook.get_latest_video')
# @patch('app.webhook.send_whatsapp_message')
# def test_process_task_completion(mock_send_whatsapp, mock_get_latest_video):
#     Config.SEND_WHATSAPP_MESSAGES = False
#     mock_get_latest_video.return_value = "Test Video URL"
#     mock_send_whatsapp.return_value = "message_id_123"

#     result = process_task_completion()

#     assert result['success'] == True
#     assert result['message'] == "Task completion processed"
#     mock_get_latest_video.assert_called_once()
#     mock_send_whatsapp.assert_not_called()  # Ensure WhatsApp message is not sent

# def test_webhook_exception(client):
#     data = {
#         "type": "scored",
#         "webhookType": "taskActivity",
#         "task": {
#             "type": "daily",
#             "text": Config.TASK_TO_BE_COMPLETED
#         },
#         "direction": "up"
#     }
    
#     with patch('app.webhook.process_task_completion', side_effect=Exception("Test exception")):
#         response = client.post('/webhook', data=json.dumps(data), content_type='application/json')
#         assert response.status_code == 500
#         assert response.json['success'] == False
#         assert response.json['message'] == "Internal server error"