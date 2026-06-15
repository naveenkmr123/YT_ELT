import requests
from loguru import logger
import os
from dotenv import load_dotenv
from datetime import date
import json

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



def get_video_data(video_ids):

    extracted_data = []
    batch_size = 50
    batch_count = 0
    def batch_list(video_id_lst, batch_size):
          for video in range(0, len(video_id_lst), batch_size):
               yield video_id_lst[video : video+batch_size]
    try:
        for batch in batch_list(video_ids, batch_size):  
            video_id_str = ",".join(batch)
            
            batch_count += 1

            URL = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=Snippet&part=Statistics&id={video_id_str}&key={API_KEY}"

            response = requests.get(URL)

            data = response.json()

            for item in data.get('items', []):
                
                video_id = item['id']
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id": video_id,
                    "published_at": snippet['publishedAt'],
                    "title": snippet['title'],
                    "duration": content_details['duration'],
                    "view_count": statistics.get('viewCount', None),
                    "like_count": statistics.get('likeCount', None),
                    "comment_count": statistics.get('commentCount', None),
                }
                extracted_data.append(video_data)
            logger.info(f"Data extracted for Batch: {batch_count}")

        return extracted_data
        
    except requests.exceptions.RequestException as e:
         raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_ELT_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
         json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)
         
if __name__ == "__main__":
    logger.info("Getting PlaylistID...")
    playlist_id = get_playlist_id()

    logger.info("Getting Video IDs...")
    video_ids = get_video_id(playlist_id)

    logger.info("Getting Video Data...")
    video_data = get_video_data(video_ids)

    logger.info("Saving Into a File...")
    save_to_json(video_data)
