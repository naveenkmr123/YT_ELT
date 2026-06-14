import requests
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
CHANNEL = "MrBeast2"

def get_playlist_id():

    try:
        URL = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL}&key={API_KEY}"

        response = requests.get(URL)

        data = response.json()

        content_details = data["items"][0]["contentDetails"]
        playlist_id = content_details["relatedPlaylists"]['uploads']

        logger.info(f"Extracted PlaylistId: {playlist_id}")

        return playlist_id
    
    except Exception as e:
        raise e
    
def get_video_id(playlist_id):
    video_ids = []
    max_results = 50
    page_token = None
    page_count = 0

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"

    try: 
        
        while True:
                URL = base_url

                if page_token:
                    URL += f"&pageToken={page_token}"
                page_count += 1

                logger.info(f"Page count: {page_count}")
                response = requests.get(URL)

                data = response.json()

                for item in data.get('items', []):

                    video_id = item['contentDetails']['videoId']
                    video_ids.append(video_id)    
                
                page_token = data.get('nextPageToken')
                
                if not page_token:
                    break

        return video_ids
        
    except requests.exceptions.Request as e:
            raise e

if __name__ == "__main__":
    logger.info("Getting PlaylistID")
    playlist_id = get_playlist_id()
    get_video_id(playlist_id)
