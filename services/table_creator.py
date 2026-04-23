from config.db import get_connection, get_cursor, close_all


class TableCreator:

    @staticmethod
    def create_table(model):
        table_name = model.TABLE_NAME
        schema = model.SCHEMA

        columns = ", ".join([f"{k} {v}" for k, v in schema.items()])

        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"

        conn = get_connection()
        cursor = get_cursor(conn)

        cursor.execute(query)
        conn.commit()

        close_all(cursor, conn)