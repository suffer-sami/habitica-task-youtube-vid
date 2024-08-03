from pyyoutube import Client, Api
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
CHANNEL_ID = "UC-lHJZR3Gqxm24_Vd_AJ5Yw"

def get_latest_video(api_key, channel_id):
    api = Api(api_key=api_key)
    
    # Get the channel's uploads playlist ID
    channel_info = api.get_channel_info(channel_id=channel_id)
    uploads_playlist_id = channel_info.items[0].contentDetails.relatedPlaylists.uploads

    # Get the latest video from the uploads playlist
    playlist_items = api.get_playlist_items(playlist_id=uploads_playlist_id, count=1)
    
    latest_video = playlist_items.items[0]
    published_date = latest_video.contentDetails.videoPublishedAt
    video_id = latest_video.contentDetails.videoId
    return video_id, published_date

# Call the function and print the result
latest_video_id, published_date = get_latest_video(API_KEY, CHANNEL_ID)
print(f"Latest video id: {latest_video_id}")
print(f"Published At: {published_date}") # Published At: 2024-07-24T17:00:18Z