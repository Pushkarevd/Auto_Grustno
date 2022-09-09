from db_module import connector as cn
from grustno import grustno_api as gr_api

params = {
    'database': 'd25e0t64l9dmrk',
    'host': 'ec2-3-223-242-224.compute-1.amazonaws.com',
    'user': 'xrrhghlboqjmce',
    'port': '5432',
    'password': '44b1e4189704f6e325b297a759b0668e6f6b720c04536aeb819bc6b55b5287dd'
}

get_subs = """
    SELECT name FROM SUBS;
"""


class Stats:

    def __init__(self):
        self.connector = cn.Connector(**params)
        self.grustno_instance = gr_api.Grustno()

    def get_new_subs(self):
        old_subs = set(self.connector.execute_command(get_subs))
        all_subs = set(self.grustno_instance.get_subs())
        print(old_subs - all_subs)

test = Stats()
test.get_new_subs()