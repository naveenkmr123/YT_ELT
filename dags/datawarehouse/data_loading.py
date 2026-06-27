import json
from loguru import logger
from datetime import date

def load_data():
    file_path = f"./data/YT_ELT_{date.today()}.json"

    try:
        logger.info(f"Processing file YT_ELT_{date.today()}")

        with open(file_path, "r", encoding="utf-8") as raw_data:
            data = json.load(raw_data)
        return data

    except Exception as e:
        logger.error(f"Error while loading the data YT_ELT_{date.toda()}")
        raise e    
     