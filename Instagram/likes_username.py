import json
import requests

from InstagramAPI import InstagramAPI

class instagram(object):
    def __init__(self):
        self.ig = None
        try:
            self.password = "mikhail.polosukhin2167"
            self.username = "mikhail.polosukhin216"
        except Exception as e:
            print(e)

    def instagramAPI_login(self):
        try:
            self.ig_api = InstagramAPI(self.username, self.password)
            self.ig_api.login()
        except Exception as e:
            print(e)

    def likes_username(self):
        session = requests.session()

        # LogIn for Instagram
        self.ig_login(session)

        # Following
        self.suggested_following(session)

        session.close()
        return None

    def suggested_following(self, session):
        user_names = []
        referer_url = "https://www.instagram.com/explore/people/suggested/"

        session.headers['Referer'] = referer_url
        url = "https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={variables}"
        query_hash = "d5d763b1e2acf209d62d22d184488e57"
        input_pic_url = "https://www.instagram.com/p/B2gyBi-lNK_/"
        shortcode = input_pic_url.split('/')[-2].strip()
        variables = {"shortcode": shortcode,"include_reel": "true","first": 12, "after": ""}
        has_next_page = True
        try:
            while True:
                if has_next_page:
                    req_url = url.format(query_hash=query_hash, variables=json.dumps(variables))
                    resp = session.get(req_url).text
                    user_data = json.loads(resp).get('data', {}).get('shortcode_media', {}).get('edge_liked_by', {})
                    suggested_user = user_data.get('edges', [])
                    after_cursor = user_data.get('page_info', {}).get('end_cursor')
                    has_next_page = user_data.get('page_info', {}).get('has_next_page')

                    for s in suggested_user:
                        user_names.append(s.get('node', {}).get('username') + '\n')

                    variables['after'] = after_cursor
                else:
                    break
        except Exception as e:
            print(e)

        if user_names:
            file1 = open("likes_usernames.txt", "w")
            file1.writelines(user_names)

    def ig_login(self, session):
        login_url = "https://www.instagram.com/accounts/login/ajax/"
        BASE_URL = "https://www.instagram.com/"

        login_data = {"username": self.username, "password": self.password}
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/76.0.3809.100 Safari/537.36"

        session.headers = {'user-agent': user_agent, 'Referer': BASE_URL}
        try:
            resp = session.get(BASE_URL)

            session.headers.update({'X-CSRFToken': resp.cookies['csrftoken']})
            login_resp = session.post(login_url, data=login_data, allow_redirects=True)
            if login_resp.json()['authenticated']:
                print("Login successful, username: {}, password: {}".format(self.username, self.password))
            else:
                print("Login failed!, username: {}, password: {}".format(self.username, self.password))
        except Exception as e:
            print(e, "Login Error, username: {} password: {}".format(self.username, self.password))
        session.headers.update({'X-CSRFToken': login_resp.cookies['csrftoken']})

        return


def main(event, context):
    u = instagram()
    u.likes_username()
if __name__ == "__main__":
    main(0, 0)