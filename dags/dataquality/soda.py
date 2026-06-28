from loguru import logger
from airflow.operators.bash import BashOperator

SODA_PATH = '/opt/airflow/include/soda'
DATASOURCE = 'pg_datasource'

def yt_data_quality(schema_name):
    try:
        task = BashOperator(
            task_id = f"soda_test_{schema_name}",
            bash_command = f"soda scan -d {DATASOURCE} -c {SODA_PATH}/configuration.yml -v SCHEMA={schema_name} {SODA_PATH}/checks.yml",
        )

        return task
    
    except Exception as e:
        logger.error("Error while data quality test.")
        raise e
