from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table_name = "yt_api"

#connection
def get_conn_cur():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    return conn, cur

#close connection
def close_conn(conn, cur):

    cur.close()
    conn.close()

#create schema
def create_schema(schema_name):
    
    conn, cur = get_conn_cur()

    schema_sql = f"""
            CREATE SCHEMA IF NOT EXISTS {schema_name};
        """
    cur.execute(schema_sql)
    conn.commit()

    close_conn(conn, cur)

#create table
def create_table(schema_name):
    conn, cur = get_conn_cur()

    if schema_name == "staging":
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "video_title" TEXT NOT NULL,
                "upload_date" TIMESTAMP NOT NULL,
                "duration" VARCHAR(11) NOT NULL,
                "view_count" INT,
                "like_count" INT,
                "comment_count" INT
                )
            """
    else:
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
                "video_id" VARCHAR(11) PRIMARY KEY NOT NULL,
                "video_title" TEXT NOT NULL,
                "upload_date" TIMESTAMP NOT NULL,
                "duration" INT NOT NULL,
                "video_type" VARCHAR(11) NOT NULL,
                "view_count" INT,
                "like_count" INT,
                "comment_count" INT
                )
            """
    cur.execute(table_sql)

    conn.commit()

    close_conn(conn, cur)

#get video Ids

def get_video_ids(cur, schema_name):

    cur.execute(f"""SELECT "video_id" from {schema_name}.{table_name};""")
    ids = cur.fetchall()

    video_ids = [row["video_id"] for row in ids]

    return video_ids
