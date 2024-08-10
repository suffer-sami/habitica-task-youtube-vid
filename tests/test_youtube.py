# tests/test_youtube.py

from app.youtube import get_latest_video

def test_get_latest_video(mocker):
    # Mock the Api call
    mock_api = mocker.patch('app.youtube.Api', autospec=True)

    # Create a mock for the video id
    mock_channel_info = mocker.Mock()
    mock_channel_info.items = [
        mocker.Mock(contentDetails=mocker.Mock(relatedPlaylists=mocker.Mock(uploads='UPLOADS_PLAYLIST_ID')))
    ]

    mock_playlist_items = mocker.Mock()
    mock_playlist_items.items = [
        mocker.Mock(contentDetails=mocker.Mock(videoId='VIDEO_ID'))
    ]

    mock_api.return_value.get_channel_info.return_value = mock_channel_info
    mock_api.return_value.get_playlist_items.return_value = mock_playlist_items

    video_url = get_latest_video()

    assert video_url == "https://www.youtube.com/watch?v=VIDEO_ID"

def test_get_latest_video_no_videos(mocker):
    # Mock the Api call
    mock_api = mocker.patch('app.youtube.Api', autospec=True)

    # Mocking the API response with no videos
    mock_api.return_value.get_channel_info.return_value.items = [
        mocker.Mock(contentDetails=mocker.Mock(relatedPlaylists=mocker.Mock(uploads='UPLOADS_PLAYLIST_ID')))
    ]
    mock_api.return_value.get_playlist_items.return_value.items = []

    video_url = get_latest_video()
    assert video_url is None