from app.whatsapp import send_whatsapp_message


def test_send_whatsapp_message_success(mocker):
    mock_client = mocker.patch('app.whatsapp.Client', autospec=True)
    mock_message = mocker.Mock()
    mock_message.sid = 1
    mock_client.return_value.messages.create.return_value = mock_message

    result = send_whatsapp_message("Test message")
    assert result == 1
    mock_client.return_value.messages.create.assert_called_once()


def test_send_whatsapp_message_exception(mocker):
    mock_client = mocker.patch('app.whatsapp.Client', autospec=True)
    mock_client.return_value.messages.create.side_effect = Exception(
        "Twilio error")

    result = send_whatsapp_message("Test message")
    assert result is None
    mock_client.return_value.messages.create.assert_called_once()
