from grustno import grustno_api as gr_api
from statistics import stats as st
from time import sleep
from datetime import datetime
from db_module.update_db import create_update_command, check_like
from db_module.connector import Connector

params = {
    'database': 'd25e0t64l9dmrk',
    'host': 'ec2-3-223-242-224.compute-1.amazonaws.com',
    'user': 'xrrhghlboqjmce',
    'port': '5432',
    'password': '44b1e4189704f6e325b297a759b0668e6f6b720c04536aeb819bc6b55b5287dd'
}


def like_all_posts(instance: gr_api.Grustno, diff_set_hot: list, diff_set_unknown: list, connector: Connector) -> None:
    def set_likes(posts, diff_set):
        for post in posts:
            post_id = post.get('id')

            if post_id not in diff_set:

                command = check_like(post_id)
                if not connector.execute_command(command):
                    print(f'{post_id} check passed')
                    command = create_update_command(post_id, datetime.now())
                    connector.execute_command(command)

                diff_set.append(post_id)
                instance.like(post_id)

    set_likes(instance.get_list_posts(), diff_set_unknown)
    set_likes(instance.get_hot_posts(), diff_set_hot)


def check_diff_sets(diff_set_hot: list, diff_set_unknown: list) -> tuple[list, list]:
    if len(diff_set_hot) >= 50:
        diff_set_hot = diff_set_hot[25:]

    if len(diff_set_unknown) >= 50:
        diff_set_unknown = diff_set_unknown[25:]
    return diff_set_unknown, diff_set_hot


if __name__ == "__main__":
    instance = gr_api.Grustno()
    counter = 0
    diff_set_unknown = []
    diff_set_hot = []
    connector = Connector(**params)
    while True:
        like_all_posts(instance, diff_set_hot, diff_set_unknown, connector)
        sleep(10)
        diff_set_unknown, diff_set_hot = check_diff_sets(diff_set_hot, diff_set_unknown)
