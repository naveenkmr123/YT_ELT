from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_playlist_id, get_video_id, get_video_data, save_to_json

from datawarehouse.dwh import staging_table, core_table

#Define the local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

default_args = {
    "owner": "Naveen",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "naveen.fbara22@gmail.com",
    "retry": 2,
    "retyr_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 6, 20, tzinfo=local_tz)
    #"end_date": datetime(2026, 6, 25, tzinfo=local_tz)
}

#DAG 1: Produce JSON
with DAG(
    dag_id = "produce_json",
    default_args= default_args,
    description="DAG to produce JSON file with raw data",
    schedule= "0 19 * * *",
    catchup=False

) as dag_produce:
    
    #define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    video_data = get_video_data(video_ids)
    save_to_json_task = save_to_json(video_data)

    #define dependencies
    playlist_id >> video_ids >> video_data >> save_to_json_task

#DAG 2: Update DB
with DAG(
    dag_id ="update_db",
    default_args = default_args,
    description = "DAG to process JSON file and Insert/Update DB",
    catchup = False,
    schedule = None
) as dag_update:
    
    #define tasks
    update_staging = staging_table()
    update_core = core_table()

    #define dependencies
    update_staging >> update_core
 

