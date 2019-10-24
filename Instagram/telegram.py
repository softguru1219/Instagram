import os
import re
import json
import time
import instaloader
import requests

from datetime import datetime
from urllib.parse import urlencode
from InstagramAPI import InstagramAPI

class telegram(object):
    def write_comments(self):
        username = "seanp.gustafson25"
        password = "NM5F18Ez08fU"
        # u = upload(acc['username'], acc['password'])
        session = requests.session()
        headers = {
            "Host": "www.instagram.com",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.instagram.com/accounts/edit/",
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
        }

        # LogIn for Instagram
        self.ig_login(session)

        # Post commnets
        self.post_comments(session, headers)

    def ig_login(self, session):
        login_url = "https://www.instagram.com/accounts/login/ajax/"
        BASE_URL = "https://www.instagram.com/"

        login_data = {"username": "seanp.gustafson25", "password": "NM5F18Ez08fU"}
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/76.0.3809.100 Safari/537.36"

        session.headers = {'user-agent': user_agent, 'Referer': BASE_URL}
        resp = session.get(BASE_URL)

        session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
        login_resp = session.post(login_url, data=login_data, allow_redirects=True)
        if login_resp.json()['authenticated']:
            print("Login successful")
        else:
            print("Login failed!")
            self.ig_login()

        session.headers.update({'X-CSRFToken': login_resp.cookies['csrftoken']})
        return

    def post_comments(self, session, headers):
        user_id = None
        session.headers.update(headers)
        ig_user_url = "https://www.instagram.com/p/B14NcTUFzOG/"
        try:
            session.headers.update({'Referer': ig_user_url})
            resp = requests.get(ig_user_url)
            session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
            if resp.status_code == 200:
                user_id = self.get_user_id(resp)
            if user_id:
                self.w_comments(user_id, session)

        except Exception as e:
            print(e)
        return

    def get_user_id(self, resp):
        user_id = None
        try:
            d = re.search('window._sharedData = (.*?);', resp.text, re.DOTALL)
            json_data = json.loads(d) if d else None
            user_id = json_data.get('entry_data', {}).get('PostPage')[0].get('graphql', {}).get('shortcode_media', {}).get('id')
        except Exception as e:
            print(e)
        return user_id

    def w_comments(self, user_id, session):
        post_url = 'https://www.instagram.com/web/comments/%s/add/'
        post_url = post_url % str(user_id)
        data = {}
        try:
            resp = session.post()
        except Exception as e:
            print(e)

def main(event, context):
    t = telegram()
    t.write_comments()

if __name__ == "__main__":
    main(0, 0)