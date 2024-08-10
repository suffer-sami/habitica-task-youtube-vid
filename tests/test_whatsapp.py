# tests/test_whatsapp.py

from app.whatsapp import send_whatsapp_message

def test_send_whatsapp_message(mocker):
    # Mock the Config
    mock_config = mocker.patch('app.whatsapp.Config')
    
    # Mock the Twilio Client
    mock_client = mocker.Mock()
    mock_message = mocker.Mock()
    mock_message.sid = "test_message_sid"
    mock_client.messages.create.return_value = mock_message
    mocker.patch('app.whatsapp.Client', return_value=mock_client)

    # Test when SEND_WHATSAPP_MESSAGES is False
    mock_config.SEND_WHATSAPP_MESSAGES = False
    result = send_whatsapp_message("Test message")
    assert result == 0
    mock_client.messages.create.assert_not_called()

    # Test when SEND_WHATSAPP_MESSAGES is True
    mock_config.SEND_WHATSAPP_MESSAGES = True
    result = send_whatsapp_message("Test message")
    assert result == "test_message_sid"
    mock_client.messages.create.assert_called_once()

    # Reset the mock to clear the call count
    mock_client.messages.create.reset_mock()

    # Test exception handling
    mock_client.messages.create.side_effect = Exception("Twilio error")
    result = send_whatsapp_message("Test message")
    assert result == 0
    mock_client.messages.create.assert_called_once()