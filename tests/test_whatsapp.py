# tests/test_whatsapp.py

from app.whatsapp import send_whatsapp_message

def test_send_whatsapp_message(mocker):
    mock_config = mocker.patch('app.whatsapp.Config', autospec=True)
    mock_config.SEND_WHATSAPP_MESSAGES = False

    mock_twilio_client = mocker.patch('app.whatsapp.Client', autospec=True)

    result = send_whatsapp_message("Test message")

    assert result == 0
    mock_twilio_client.assert_not_called()
