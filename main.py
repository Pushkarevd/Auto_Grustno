import requests
import os
from time import sleep


API = "https://api.grustnogram.ru"


class Grustno:
    headers = {
        "user-agent": "Dart/2.16 (dart:io)"
    }

    def __init__(self):
        self.login()

    def login(self):
        data = {
            "email": os.environ['mail'],
            "password": os.environ['password']
        }
        response = requests.post(
            f"{API}/sessions",
            json=data,
            headers=self.headers).json()
        access_token = response["data"]["access_token"]
        self.headers["access-token"] = access_token

    def like(self, post_id: int):
        api = f'https://api.grustnogram.ru/posts/{post_id}/like'
        requests.post(api, data={}, headers=self.headers)

    def get_list_posts(self):
        api = API + '/posts?my=2&hell=1'
        return requests.get(api, headers=self.headers).json()['data'][:50]


def main():
    instance = Grustno()
    while True:
        posts = instance.get_list_posts()
        for post in posts:
            post_id = post.get('id')
            instance.like(post_id)
        sleep(10)


print('App is running')
main()
