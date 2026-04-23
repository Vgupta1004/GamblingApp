from config.db import get_connection, get_cursor, close_all

class SchemaService:
    @staticmethod
    def create_table(entity):
        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = get_cursor(connection)

            columns_sql = ",\n    ".join(
                f"{col_name} {col_def}"
                for col_name, col_def in entity.COLUMNS
            )

            sql = f"CREATE TABLE IF NOT EXISTS {entity.TABLE_NAME} ({columns_sql})"

            cursor.execute(sql)
            connection.commit()
        finally:
            close_all(cursor, connection)