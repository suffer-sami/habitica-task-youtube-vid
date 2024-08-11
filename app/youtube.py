import logging
from pyyoutube import Api
from .config import Config


def get_latest_video():
    try:
        api = Api(api_key=Config.YOUTUBE_API_KEY)
        channel_info = api.get_channel_info(
            for_handle=Config.YOUTUBE_CHANNEL_HANDLE)

        if not channel_info.items:
            logging.error("No channel information found.")
            return None

        content_details = channel_info.items[0].contentDetails
        uploads_playlist_id = content_details.relatedPlaylists.uploads

        # Get the latest video from the uploads playlist
        playlist_items = api.get_playlist_items(
            playlist_id=uploads_playlist_id, count=1)

        if not playlist_items.items:
            logging.info("The uploads playlist has no videos.")
            return None

        latest_video = playlist_items.items[0]
        video_id = latest_video.contentDetails.videoId
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
