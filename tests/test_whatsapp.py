from app.whatsapp import send_whatsapp_message


def test_send_whatsapp_message_enabled(mocker):
    mock_client = mocker.patch('app.whatsapp.Client', autospec=True)
    mock_config = mocker.patch('app.whatsapp.Config')
    mock_config.SEND_WHATSAPP_MESSAGES = True

    mock_message = mocker.Mock()
    mock_message.sid = 1
    mock_client.return_value.messages.create.return_value = mock_message

    result = send_whatsapp_message("Test message")
    assert result == 1


def test_send_whatsapp_message_disabled(mocker):
    mock_client = mocker.patch('app.whatsapp.Client', autospec=True)
    mock_config = mocker.patch('app.whatsapp.Config')
    mock_config.SEND_WHATSAPP_MESSAGES = False

    result = send_whatsapp_message("Test message")
    assert result == 0
    mock_client.messages.create.assert_not_called()


def test_send_whatsapp_message_exception(mocker):
    mock_client = mocker.patch('app.whatsapp.Client', autospec=True)
    mock_config = mocker.patch('app.whatsapp.Config')
    mock_config.SEND_WHATSAPP_MESSAGES = True

    mock_client.return_value.messages.create.side_effect = Exception(
        "Twilio error")
    result = send_whatsapp_message("Test message")
    assert result is None
    mock_client.return_value.messages.create.assert_called_once()
