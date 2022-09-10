from grustno import grustno_api as gr_api
from time import sleep
from datetime import datetime
from db_module.update_db import create_update_command, check_like
from db_module.connector import Connector
from os import environ
from subs_module.load_subs import update_subs

params = {
    'database': 'grustno_bot',
    'user': 'grustno_bot',
    'password': 'no1trol',
    'host': '192.168.0.137',
    'port': '5432'
}


def like_all_posts(instance: gr_api.Grustno, diff_set_hot: list, diff_set_unknown: list, connector: Connector) -> None:
    def set_likes(posts, diff_set):
        for post in posts:
            post_id = post.get('id')
            username = post.get('user').get('nickname')

            if post_id not in diff_set:

                command = check_like(post_id)
                if not connector.execute_command(command):
                    command = create_update_command(post_id, datetime.now(), username)
                    print(f'Post from {username} - {post_id} liked at {datetime.now()}')
                    connector.execute_command(command)

                diff_set.append(post_id)
                print(instance.like(post_id))
                sleep(.2)
                instance.like(post_id)
        for post in posts:
            post_id = post.get('id')
            instance.like(post_id)
            sleep(.2)
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
    diff_set_unknown = []
    diff_set_hot = []
    connector = Connector(**params)
    counter = 0
    while True:
        like_all_posts(instance, diff_set_hot, diff_set_unknown, connector)
        sleep(10)
        counter += 1
        diff_set_unknown, diff_set_hot = check_diff_sets(diff_set_hot, diff_set_unknown)
        if counter == 6:
            counter = 0
            update_subs(instance, connector)

