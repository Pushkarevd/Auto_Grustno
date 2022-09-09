import psycopg2 as pg


class Connector:

    def __init__(self, host: str, database: str, user: str, port: int, password: str):
        self.conn = pg.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = True

    def execute_command(self, command: str):
        with self.conn.cursor() as curr:
            curr.execute(command)
            try:
                records = curr.fetchall()
                return records
            except pg.ProgrammingError:
                pass

    def __del__(self):
        self.conn.close()