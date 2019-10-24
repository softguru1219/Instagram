import os
import re
import time
import json
import random
import requests
import pandas as pd
from instabot import Bot
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from random import randint
from time import sleep, strftime
from InstagramAPI import InstagramAPI
# from instabot_py.instabot import InstaBot

def send_delayed_keys(element, text, delay=0.3) :
    for c in text :
        endtime = time.time() + delay
        element.send_keys(c)
        time.sleep(endtime - time.time())

class instagram(object):
    def __init__(self, e_data, u_data, exist_data):
        self.ig = None
        try:
            self.name = e_data['name']
            self.username = e_data['username']
            self.password = e_data['password']
            self.email = e_data['email']
            # self.password = "NM5F18Ez08fU"
            # self.username = "cregsxander25"
            # self.email = "seanp.gustafson25@gmail.com"
            self.gender = u_data['MALE/FEMALE']
            self.u_data = u_data
            self.exist_data = exist_data
        except Exception as e:
            print(e)

    # Upload photo
    def post_photo(self):
        self.instagramAPI_login()
        current_path = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_path, os.pardir))
        try:
            post_images_path = parent_dir + "\\post_photos"
            pic_list = []
            for s_path, s_dirs, s_files in os.walk(post_images_path):
                try:
                    idxs = self.Rand(0, len(s_files) - 1, 6)
                    pic_list = [os.path.join(s_path, s_files[i]) for i in idxs if os.path.isfile(os.path.join(s_path, s_files[i]))]
                    pic_list = list(set(pic_list))
                except Exception as e:
                    print(e, "Error when choice the pic, username: {}, password: {}".format(self.username, self.password))
            for pic in pic_list:
                try:
                    if pic.endswith('jpg'):
                        self.ig_api.uploadPhoto(pic, caption='image')
                        # os.remove(pic)
                        print("Posted the images successfully, pic: {}".format(pic))
                except Exception as e:
                    print(e, "Error when choice the pic, username: {}, password: {}, pic: {}".format(self.username, self.password, pic))
                    continue
                time.sleep(3)
        except Exception as e:
            print(e)

        self.ig_api.logout()

    def instagramAPI_login(self):
        try:
            self.ig_api = InstagramAPI(self.username, self.password)
            self.ig_api.login()
        except Exception as e:
            print(e)

    # User Following
    def user_following(self, user_ids):
        self.instagramAPI_login()
        current_followings = self.ig_api.getTotalSelfFollowings()
        exist_following_ids = []
        if current_followings:
            try:
                exist_following_ids = [str(cf.get('pk')) for cf in current_followings if cf.get('pk')]
            except Exception as e:
                print(e, 'Error when check the existing followings')

        if user_ids:
            for ui in user_ids:
                if exist_following_ids:
                    if not ui in exist_following_ids:
                        self.ig_api.follow(ui)
                        print("Followed the {}".format(str(ui)))
                else:
                    self.ig_api.follow(ui)
                    print("Followed the {}".format(str(ui)))
        else:
            idxs = self.Rand(0, len(self.exist_data), 3)
            for i in idxs:
                d = self.exist_data[i]
                if d.get('username') != self.username:
                    try:
                        user_id = self.get_user_info(d.get('username'))
                        if user_id:
                            if exist_following_ids:
                                if not user_id in exist_following_ids:
                                    self.ig_api.follow(user_id)
                                    print("Followed the {}".format(d.get('username')))
                            else:
                                self.ig_api.follow(user_id)
                                print("Followed the {}".format(d.get('username')))
                    except Exception as e:
                        print(e, "Error when follow the {}".format(d.get('username')))
                        pass
        self.ig_api.logout()

    def edit_profile(self):
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

        # Change profile picture
        # self.ig_change_picture(session, headers)

        # Change profile gender
        # self.ig_change_gender(session, headers)

        # Change profile name, username and bio
        # updated_data = self.ig_change_username(session, headers)

        # Setting Private
        # self.set_private(session, headers)

        # Following
        # self.suggested_following(session)

        session.close()
        return None

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

    def suggested_following(self, session):
        user_ids = []
        start_count = 0
        total_count = 30
        referer_url = "https://www.instagram.com/explore/people/suggested/"

        session.headers['Referer'] = referer_url
        url = "https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={variables}"
        query_hash = "bd90987150a65578bc0dd5d4e60f113d"
        variables = {"fetch_media_count": start_count, "fetch_suggested_count": total_count, "ignore_cache": "true",
                    "filter_followed_friends": "true", "seen_ids": [], "include_reel": "true"}
        try:
            while True:
                if start_count < 120:
                    variables["fetch_media_count"] = start_count
                    variables["fetch_suggested_count"] = total_count

                    req_url = url.format(query_hash=query_hash, variables=json.dumps(variables))
                    resp = session.get(req_url).text
                    user_data = json.loads(resp).get('data', {}).get('user', {})
                    suggested_user = user_data.get('edge_suggested_users', {}).get('edges', [])
                    for s in suggested_user:
                        user_ids.append(s.get('node', {}).get('user', {}).get('id'))
                    start_count += 30
                    total_count += 30
                else:
                    break
        except Exception as e:
            print(e)

        if user_ids:
            user_ids = list(set(user_ids))
            self.user_following(user_ids)

    def ig_change_username(self, session, headers):
        CHANGE_URL = "https://www.instagram.com/accounts/edit/"
        session.headers.update(headers)
        bio = self.u_data.get('BIO')
        if len(bio) > 150:
            bio = bio[:150]
        CHNAGE_DATA = {"first_name": self.u_data.get('NAME'), "email": self.email, "username": self.u_data.get('@ USERNAME'),
                       "biography": bio}


        session.headers.update(headers)
        updated_data = []
        try:
            for i in range(3):
                r = session.post(CHANGE_URL, data=CHNAGE_DATA)
                if r.json()['status'] == 'ok':
                    print("Profile name and bio, username changed!, new_user_name: {}".format(self.u_data.get('@ USERNAME')))
                    self.u_data['PASSWORD'] = self.password
                    break
                else:
                    print(r.json()['message']['errors'][0])
                    num = random.randint(1, 100)
                    self.u_data['@ USERNAME'] = self.u_data.get('@ USERNAME') + '_' + str(num)
                    CHNAGE_DATA['username'] = self.u_data['@ USERNAME']
        except Exception as e:
            print(e, "origin_username: {}, username: {}, name: {}, password: {}".format(self.username, self.u_data.get('@ USERNAME'), self.u_data.get('NAME'), self.password))
            pass
        # print(r.text)
        return updated_data

    def ig_change_picture(self, session, headers):
        X_SECOND = 10
        CHANGE_URL = "https://www.instagram.com/accounts/web_change_profile_picture/"
        CHNAGE_DATA = {"Content-Disposition": "form-data", "name": "profile_pic", "filename": "profilepic.jpg",
                       "Content-Type": "image/jpeg"}

        session.headers.update(headers)
        p_pic = self.u_data.get('PIC')
        try:
            if p_pic:
                p_pic_s = os.path.getsize(p_pic)
                session.headers.update({'Content-Length': str(p_pic_s)})
                files = {'profile_pic': open(p_pic, 'rb')}

                r = session.post(CHANGE_URL, files=files, data=CHNAGE_DATA)
                if r.json()['changed_profile']:
                    print("Profile picture changed!")
                else:
                    print("Something went wrong")
                time.sleep(X_SECOND)
        except Exception as e:
            print(e, "Profile picture Error, username: {} , password: {}".format(self.username, self.password))
            pass
        # print(r.text)

    def ig_change_gender(self, session, headers):
        CHANGE_URL = "https://www.instagram.com/accounts/set_gender/"
        session.headers.update(headers)
        if self.gender:
            if self.gender.lower().startswith('m'):
                gender = 1
            elif self.gender.lower().startswith('f'):
                gender = 2

        CHANGE_DATA = {"gender": gender, 'custom_gender': ''}
        session.headers.update(headers)

        try:
            r = session.post(CHANGE_URL, data=CHANGE_DATA)
            if r.json()['status'] == 'ok':
                print("gender changed!")
            else:
                print(r.json()['message']['errors'][0])
        except Exception as e:
            print(e, "gender Error, username: {} , password: {}".format(self.username, self.password))
            pass
        print(r.text)

    def set_private(self, session, headers):
        CHANGE_URL = "https://www.instagram.com/accounts/set_private/"
        session.headers.update(headers)
        CHNAGE_DATA = {"is_private": "true"}
        headers['Referer']= "https://www.instagram.com/accounts/privacy_and_security/"
        session.headers.update(headers)
        try:
            for i in range(3):
                r = session.post(CHANGE_URL, data=CHNAGE_DATA)
                if r.json()['status'] == 'ok':
                    print("Set to private, username: {}".format(self.username))
                    break
                else:
                    print(r.json()['message']['errors'][0])

        except Exception as e:
            print(e, "origin_username: {}, username: {}, name: {}, password: {}".format(self.username,
                                                                                        self.u_data.get('@ USERNAME'),
                                                                                        self.u_data.get('NAME'),
                                                                                        self.password))
            pass
        return

    def special_user_following(self):
        user_ids = ["18428286"]
        self.instagramAPI_login()
        try:
            if user_ids:
                for ui in user_ids:
                    self.ig_api.follow(ui)
                    print("Followed the {}".format(str(ui)))
        except Exception as e:
            print("Error when follow the special user , username {}".format(self.username))
        self.ig_api.logout()
        sleep(20)

    def instabot_login(self):
        try:
            bot = Bot()
            bot.login(username=self.username, password=self.password)
            csv_file = 'verify.csv'
            user_name = "donny.aldcollins"
            # users = self.csv_to_json(csv_file)
            user_ids = self.get_user_info(user_name)
            bot.follow_users(user_ids)
        except Exception as e:
            print(e)
        bot

    def selenium_user_following(self):
        self.instagram_login_with_selenium()

    def instagram_login_with_selenium(self):
        DRIVER = 'CHROME'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        sleep(2)
        driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        sleep(3)

        action_chains = ActionChains(driver)
        username_field = driver.find_element_by_name('username')
        print(username_field)
        action_chains.move_to_element(username_field)
        # username_field.send_keys(acc['username'])
        send_delayed_keys(username_field, self.username, 0.3)
        time.sleep(2)

        # Enter PASSWORD
        password_field = driver.find_element_by_name('password')
        print(password_field)
        action_chains.move_to_element(password_field)
        # password_field.send_keys(acc['password'])
        send_delayed_keys(password_field, self.password, 0.3)
        time.sleep(2)

        login_btn = driver.find_element_by_xpath("//button[@type='submit']")
        login_btn.click()
        sleep(3)

        not_now = driver.find_elements_by_xpath("//button[contains(@class, 'HoLwm')]")
        if not_now:
            try:
                not_now[0].click()
            except Exception as e:
                print(e)

    def get_user_info(self, username):
        url = 'https://www.instagram.com/{username}/?__a=1'
        url = url.format(username=username)
        user_id = None
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                user_id = resp.json().get('graphql', {}).get('user', {}).get('id')
        except Exception as e:
            print(e, 'username: {}'.format(''))

        return user_id

    def get_token_hash(self):
        get_token = None
        rollout_hash = None

        url = 'https://www.instagram.com/'
        resp = requests.get(url).text
        try:
            resp = re.search('window._sharedData = (.*?);', resp, re.DOTALL).group(1)
            get_token = json.loads(resp).get('config', {}).get('csrf_token')
            rollout_hash = json.loads(resp).get('rollout_hash')
        except Exception as e:
            print(e)

        return get_token, rollout_hash

    def Rand(self, start, end, num):
        res = []
        for j in range(num):
            res.append(random.randint(start, end))
        return res

    def csv_to_json(self, csv_file):
        import csv
        user_list = []
        with open(csv_file) as f:
            csvReader = csv.DictReader(f)
            for rows in csvReader:
                username = rows['username']
                user_list.append(username)
        return user_list

def main(event, context):
    u = instagram()

if __name__ == "__main__":
    main(0, 0)