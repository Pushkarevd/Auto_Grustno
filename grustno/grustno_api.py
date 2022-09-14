import requests
import os

API = "https://api.grustnogram.ru"


class Grustno:
    headers = {
        "user-agent": "Dart/2.16 (dart:io)"
    }
    user_id = 66845  # os.environ.get('username')

    def __init__(self):
        self.session = None
        self.login()

    def login(self):
        session = requests.Session()
        data = {
            "email": os.environ.get('mail'),
            "password": os.environ.get('password')
        }
        response = session.post(
            f"{API}/sessions",
            json=data,
            headers=self.headers).json()
        access_token = response["data"]["access_token"]
        self.headers["access-token"] = access_token
        self.session = session

    def like(self, post_id: int) -> None:
        api = f'https://api.grustnogram.ru/posts/{post_id}/like'
        self.session.post(api, data={}, headers=self.headers)

    def get_list_posts(self) -> list:
        api = API + '/posts?my=2&hell=1'
        return self.session.get(api, headers=self.headers).json()['data'][:25]

    def get_hot_posts(self) -> list:
        api = API + '/posts'
        return self.session.get(api, headers=self.headers).json()['data'][:25]

    def get_subs(self) -> list:
        subs = []
        all_subs = []
        target = self.get_self().get('data').get('followers')
        while len(all_subs) != target:
            if len(subs) == 0:
                offset = None
            else:
                offset = self.__search_user(subs[-1])

            subs = self.__get_subs(offset)
            all_subs.extend(subs)
        return all_subs

    def __search_user(self, query: str) -> int:
        # Only for subs offset
        return requests.get(
            f"{API}/users?q={query}",
            headers=self.headers).json().get('data')[0].get('id')

    def __get_subs(self, offset=None) -> list:
        if offset is not None:
            response = self.session.get(
                f"{API}/followers/{self.user_id}?id={self.user_id}&offset_id={offset}",
                headers=self.headers).json()
        else:
            response = self.session.get(
                f"{API}/followers/{self.user_id}?id={self.user_id}",
                headers=self.headers).json()
        return [user['nickname'] for user in response.get('data')]

    def get_info(self, username: str) -> dict:
        return self.session.get(
            f"{API}/users/{username}",
            headers=self.headers).json()

    def get_self(self):
        return self.session.get(f'{API}/users/self', headers=self.headers).json()
