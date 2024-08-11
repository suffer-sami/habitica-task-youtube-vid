from app.youtube import get_latest_video


def test_get_latest_video_success(mocker):
    mock_api = mocker.patch('app.youtube.Api', autospec=True)
    mock_api.return_value.get_channel_info.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(
            relatedPlaylists=mocker.Mock(uploads='UPLOADS_PLAYLIST_ID')))
    ]
    mock_api.return_value.get_playlist_items.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(videoId='VIDEO_ID'))
    ]

    video_url = get_latest_video()
    assert video_url == "https://www.youtube.com/watch?v=VIDEO_ID"


def test_get_latest_video_no_videos(mocker):
    mock_api = mocker.patch('app.youtube.Api', autospec=True)
    mock_api.return_value.get_channel_info.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(
            relatedPlaylists=mocker.Mock(uploads='UPLOADS_PLAYLIST_ID')))
    ]
    mock_api.return_value.get_playlist_items.return_value.items = []

    video_url = get_latest_video()
    assert video_url is None


def test_get_latest_video_no_channel(mocker):
    mock_api = mocker.patch('app.youtube.Api', autospec=True)
    mock_api.return_value.get_channel_info.return_value.items = []

    video_url = get_latest_video()
    assert video_url is None


def test_get_latest_video_invalid_video_data(mocker):
    mock_api = mocker.patch('app.youtube.Api', autospec=True)
    mock_api.return_value.get_channel_info.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(
            relatedPlaylists=mocker.Mock(uploads='UPLOADS_PLAYLIST_ID')))
    ]
    mock_api.return_value.get_playlist_items.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(videoId=None))
    ]

    video_url = get_latest_video()
    assert video_url is None


def test_get_latest_video_no_uploads(mocker):
    mock_api = mocker.patch('app.youtube.Api', autospec=True)
    mock_api.return_value.get_channel_info.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(
            relatedPlaylists=mocker.Mock(uploads=None)))
    ]
    mock_api.return_value.get_playlist_items.return_value.items = []

    video_url = get_latest_video()
    assert video_url is None


def test_get_latest_video_api_exception(mocker):
    mocker.patch('app.youtube.Api', side_effect=Exception("API failure"))

    video_url = get_latest_video()
    assert video_url is None
