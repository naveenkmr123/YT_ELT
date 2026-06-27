from datawarehouse.db_utils import (get_conn_cur, 
                      close_conn,
                      create_schema,
                      create_table,
                      get_video_ids)

from datawarehouse.data_loading import load_data
from datawarehouse.data_modification import insert_rows, update_rows, delete_rows
from datawarehouse.data_transformation import transformed_data
from airflow.decorators import task
from loguru import logger

table = "yt_api"

@task
def staging_table():

    schema_name = "staging"
    conn, cur = None, None

    try:

        conn, cur = get_conn_cur()

        create_schema(schema_name)
        create_table(schema_name)

        yt_data = load_data()

        table_ids = get_video_ids(cur, schema_name)
        
        #insert/update records

        for row in yt_data:

            if len(table_ids) == 0:
                insert_rows(conn, cur, schema_name, row)
            
            else:
                if row['video_id'] in table_ids:
                    update_rows(conn, cur, schema_name, row)
                else:
                    insert_rows(conn, cur, schema_name, row)
        
        #delete records

        ids_in_json = {row['video_id'] for row in yt_data}
        ids_to_delete = set(table_ids) - ids_in_json

        if ids_to_delete:
            delete_rows(conn, cur, schema_name, ids_to_delete)

    
    except Exception as e:
        logger.error("Error occured while updating staging table")
        raise e
    
    finally:
        if conn and cur:
            close_conn(conn, cur)
    

@task
def core_table():

    schema_name = "core"
    conn, cur = None, None

    try:

        conn, cur = get_conn_cur()

        create_schema(schema_name)
        create_table(schema_name)

        table_ids = get_video_ids(cur, schema_name)
        

        #get data from staging table
        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()
        current_video_ids = {row['video_id'] for row in rows}
        
        #insert/update records

        for row in rows:
            
            transformed_row = transformed_data(row)

            if len(table_ids) == 0:
                insert_rows(conn, cur, schema_name, transformed_row)
            
            else:
                
                if transformed_row['video_id'] in table_ids:
                    update_rows(conn, cur, schema_name, transformed_row)
                else:
                    insert_rows(conn, cur, schema_name, transformed_row)
        
        #delete records
        ids_to_delete = set(table_ids) - current_video_ids

        if ids_to_delete:
            delete_rows(conn, cur, schema_name, ids_to_delete)

    
    except Exception as e:
        logger.error("Error occured while updating staging table")
        raise e
    
    finally:
        if conn and cur:
            close_conn(conn, cur)
        







