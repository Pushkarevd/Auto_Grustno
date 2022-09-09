from grustno import grustno_api as gr_api
from statistics import stats as st
from time import sleep


if __name__ == "__main__":
    instance = gr_api.Grustno()
    counter = 0
    while True:
        posts = instance.get_list_posts()
        for post in posts:
            post_id = post.get('id')
            instance.like(post_id)
            print(post_id)
        posts = instance.get_hot_posts()
        for post in posts:
            post_id = post.get('id')
            instance.like(post_id)
            print(post_id)
        sleep(10)
        counter += 10
        if counter == 10800:
            instance = gr_api.Grustno()

