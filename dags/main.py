from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from api.video_stats import get_playlist_id, get_video_id, get_video_data, save_to_json
from datawarehouse.dwh import staging_table, core_table
from dataquality.soda import yt_data_quality

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

staging_schema = "staging"
core_schema = "core"

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

    trigger_dag_update = TriggerDagRunOperator(
        task_id = "trigger_dag_update",
        trigger_dag_id = "update_db"
    )

    #define dependencies
    playlist_id >> video_ids >> video_data >> save_to_json_task >> trigger_dag_update

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

    trigger_data_quality = TriggerDagRunOperator(
        task_id = "trigger_data_quality",
        trigger_dag_id = "data_quality"
    )
    #define dependencies
    update_staging >> update_core >> trigger_data_quality
 
#DAG 2: Update DB
with DAG(
    dag_id ="data_quality",
    default_args = default_args,
    description = "DAG to perform data quality checks",
    catchup = False,
    schedule = None
) as dag_update:
    
    #define tasks
    staging_check = yt_data_quality(staging_schema)
    core_check = yt_data_quality(core_schema)

    #define dependencies
    staging_check >> core_check
 
