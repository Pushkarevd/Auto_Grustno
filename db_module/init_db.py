from connector import Connector
import os

create_tables = """
    CREATE TABLE subs (
        id SERIAL PRIMARY KEY NOT NULL,
        name varchar(64) NOT NULL,
        timestamp_sub TIMESTAMP
    );
    
    CREATE TABLE likes(
        id integer PRIMARY KEY NOT NULL,
        like_time timestamp NOT NULL,
        author varchar(64)
    );
"""

check_table = """
    SELECT *
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND 
          schemaname != 'information_schema';
"""

params = {
    'database': 'grustno_bot',
    'user': 'grustno_bot',
    'password': os.environ.get('db_pass'),
    'host': os.environ.get('db_host', '127.0.0.1'),
    'port': '5432'
}


class DbInitializer:

    def __init__(self):
        connector = Connector(**params)
        curr_tables = connector.execute_command(check_table)
        if len(curr_tables) == 0:
            connector.execute_command(create_tables)

DbInitializer()