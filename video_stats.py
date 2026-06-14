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

if __name__ == "__main__":
    logger.info("Getting PlaylistID")
    get_playlist_id()
