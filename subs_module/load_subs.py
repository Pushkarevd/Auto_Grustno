from db_module.connector import Connector
from grustno.grustno_api import Grustno
from datetime import datetime
import os

params = {
    'database': 'grustno_bot',
    'user': 'grustno_bot',
    'password': os.environ.get('db_pass'),
    'host': os.environ.get('db_host', '127.0.0.1'),
    'port': '5432'
}


def load_old_subs(instance: Grustno, connector: Connector):
    subs = instance.get_subs()

    for name in subs:
        load_subs = f"""
        INSERT INTO subs VALUES (DEFAULT, '{name}');
        """
        connector.execute_command(load_subs)


def update_subs(instance: Grustno, connector: Connector):
    subs_from_api = set(instance.get_subs())

    subs_from_db = set([row[1] for row in connector.execute_command("SELECT * FROM subs;")])
    # Get new subs
    new_subs = subs_from_api - subs_from_db
    # Get unsub users
    unsubed_users = subs_from_db - subs_from_api

    if not new_subs:
        return None
    for sub in new_subs:
        load_sub = f"""
        INSERT INTO subs VALUES(DEFAULT, '{sub}', '{datetime.now()}')
        """
        connector.execute_command(load_sub)
    for sub in unsubed_users:
        delete_unsubed_user = f"DELETE FROM subs WHERE name = {sub}"
        connector.execute_command(delete_unsubed_user)


if __name__ == "__main__":
    connector = Connector(**params)
    instance = Grustno()
    update_subs(instance, connector)
    #load_old_subs(instance, connector)