from loguru import logger

table_name = "yt_api"

def insert_rows(conn, cur, schema_name, row):

    if schema_name == "staging":

        insert_sql = f"""
                INSERT INTO {schema_name}.{table_name} (
                "video_id",
                "video_title",
                "upload_date",
                "duration",
                "view_count",
                "like_count",
                "comment_count"
                ) 
                VALUES (
                %(video_id)s,
                %(title)s,
                %(published_at)s,
                %(duration)s,
                %(view_count)s,
                %(like_count)s,
                %(comment_count)s
                );
            """
    
    else:
        insert_sql = f"""
                INSERT INTO {schema_name}.{table_name} (
                "video_id",
                "video_title",
                "upload_date",
                "duration",
                "video_type",
                "view_count",
                "like_count",
                "comment_count"
                ) 
                VALUES (
                %(video_id)s,
                %(video_title)s,
                %(upload_date)s,
                %(duration)s,
                %(video_type)s,
                %(view_count)s,
                %(like_count)s,
                %(comment_count)s
                );
            """
    try:

        cur.execute(insert_sql, row)
        conn.commit()

        logger.info(f"Inserted row with video id: {row['video_id']}")
    
    except Exception as e:
        logger.error(f"Error Inserting row with Video_ID: {row['video_id']} - {e}")
        raise


def update_rows(conn, cur, schema_name, row):

    if schema_name == 'staging':

        update_sql = f"""
                UPDATE {schema_name}.{table_name} 
                SET
                  "video_title" = %(title)s,
                  "upload_date" = %(published_at)s,
                  "duration" = %(duration)s,
                  "view_count" = %(view_count)s,
                  "like_count" = %(like_count)s,
                  "comment_count = %(commnet_count)s"
                WHERE "video_id" = %(video_id)s 
                AND "upload_date" = %(published_at)s;
            """
    else:

        update_sql = f"""
                UPDATE {schema_name}.{table_name} 
                SET
                  "video_title" = %(title)s,
                  "upload_date" = %(published_at)s,
                  "duration" = %(duration)s,
                  "video_type" = %(video_type)s,
                  "view_count" = %(view_count)s,
                  "like_count" = %(like_count)s,
                  "comment_count = %(commnet_count)s"
                WHERE "video_id" = %(video_id)s 
                AND "upload_date" = %(published_at)s;
            """
    
    try:

        cur.execute(update_sql, row)
        conn.commit()

        logger.info(f"Updated row with video id: {row['video_id']}")
    
    except Exception as e:
        logger.error(f"Error updating row with Video_ID: {row['video_id']} - {e}")
        raise


def delete_rows(conn, cur, schema_name, ids_to_delete):

    quoted_ids = [f"'{id}'" for id in ids_to_delete]
    ids_to_delete = f"({','.join(quoted_ids)})"

    try:
        cur.execute(
            f"""
            DELETE FROM {schema_name}.{table_name} WHERE "video_id" in %({ids_to_delete})s;
            """
        )

        conn.commit()
        logger.info(f"Deleted rows with Video_IDs: {ids_to_delete}")

    except Exception as e:
        logger.error(f"Error deleting rows with Video_IDs: {ids_to_delete}")
        raise e

