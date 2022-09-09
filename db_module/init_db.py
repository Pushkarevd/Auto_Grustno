from connector import Connector


create_tables = """
    CREATE TABLE SUBS (
        id SERIAL PRIMARY KEY,
        name varchar(64)
    );
    
    CREATE TABLE TODAY_LIKES(
        id SERIAL PRIMARY KEY,
        name varchar(64),
        like_time timestamp
    );
"""

check_table = """
    SELECT *
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND 
          schemaname != 'information_schema';
"""

params = {
    'database': 'd25e0t64l9dmrk',
    'host': 'ec2-3-223-242-224.compute-1.amazonaws.com',
    'user': 'xrrhghlboqjmce',
    'port': '5432',
    'password': '44b1e4189704f6e325b297a759b0668e6f6b720c04536aeb819bc6b55b5287dd'
}


class DbInitializer:

    def __init__(self):
        connector = Connector(**params)
        curr_tables = connector.execute_command(check_table)
        if len(curr_tables) == 0:
            connector.execute_command(create_tables)

DbInitializer()