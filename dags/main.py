from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_id, get_video_data, save_to_json

#Define the local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

default_args = {
    "owner": "Naveen",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retyr": False,
    "email": "naveen.fbara22@gmail.com",
    "retry": 2,
    "retyr_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 6, 20, tzinfo=local_tz)
    #"end_date": datetime(2026, 6, 25, tzinfo=local_tz)
}

with DAG(
    dag_id = "yt_mlt",
    default_args= default_args,
    description="DAG to produce JSON file with raw data",
    schedule= "0 19 * * *",
    catchup=False

) as dag:
    
    #define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    video_data = get_video_data(video_ids)
    save_to_json_task = save_to_json(video_data)

    #define dependencies
    playlist_id >> video_ids >> video_data >> save_to_json_task

 

