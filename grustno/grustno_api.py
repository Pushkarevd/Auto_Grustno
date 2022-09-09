import requests
import os
from time import sleep


API = "https://api.grustnogram.ru"


class Grustno:
    headers = {
        "user-agent": "Dart/2.16 (dart:io)"
    }
    user_id = 66845 #os.environ.get('username')

    def __init__(self):
        self.login()

    def login(self):
        data = {
            "email": 'willyphoto372@gmail.com',
            "password": 'Papoogtv2523'
        }
        response = requests.post(
            f"{API}/sessions",
            json=data,
            headers=self.headers).json()
        access_token = response["data"]["access_token"]
        self.headers["access-token"] = access_token

    def like(self, post_id: int) -> None:
        api = f'https://api.grustnogram.ru/posts/{post_id}/like'
        requests.post(api, data={}, headers=self.headers)

    def get_list_posts(self) -> list:
        api = API + '/posts?my=2&hell=1'
        return requests.get(api, headers=self.headers).json()['data'][:50]

    def get_hot_posts(self) -> list:
        api = API + '/posts'
        return requests.get(api, headers=self.headers).json()['data'][:50]

    def get_subs(self) -> list:
        response = requests.get(
            f"{API}/followers/{self.user_id}",
            headers=self.headers).json()
        return [user['nickname'] for user in response.get('data')]

    def get_info(self, username: str) -> dict:
        return requests.get(
            f"{API}/users/{username}",
            headers=self.headers).json()