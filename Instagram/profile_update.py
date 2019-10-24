import os
import json
import csv
import random
import time
import pandas as pd
from upload_data import instagram

class update_instagram(object):
    def update_profile(self):
        update_data = None
        exist_data = None

        try:
            f_u = open('update1.csv', encoding='utf-8')
            u_reader =  csv.DictReader(f_u, fieldnames = ( "NAME", "@ USERNAME", "MALE/FEMALE", "BIO" ))
            update_data = json.dumps([row for row in u_reader])
            update_data = json.loads(update_data)[1:]
            update_data = update_data[1:]

            f_e = open('result34.csv', encoding='utf-8')
            e_reader = csv.DictReader(f_e, fieldnames=("", "name", "username", "password", "email", "gender", "birthday"))
            exist_data = json.dumps([row for row in e_reader])
            exist_data = json.loads(exist_data)[1:]
        except Exception as e:
            print(e)

        if update_data and exist_data:
            for i, u_data in enumerate(update_data):
                try:
                    if i < len(exist_data):
                        e_data = exist_data[i]
                        gender = u_data.get('MALE/FEMALE')
                        pic = None
                        current_path = os.path.dirname(os.path.abspath(__file__))
                        parent_dir = os.path.abspath(os.path.join(current_path, os.pardir))
                        if gender and gender.lower().startswith('f'):
                            women_picture_path = os.path.join(parent_dir, "women_pictures")
                            pic = self.image_from_dir(women_picture_path)

                        if gender and gender.lower().startswith('m'):
                            man_picture_path = os.path.join(parent_dir, "man_pictures")
                            pic = self.image_from_dir(man_picture_path)

                        u_data['PIC'] = pic
                        self.upload_profile(e_data, u_data, exist_data)
                        # if pic:
                        #     os.remove(pic)
                        time.sleep(5)
                except Exception as e:
                    print(e, "profile update error")

        if os.path.exists('updated.json'):
            df = pd.read_json('updated.json')
            if os.path.exists('updated.csv'):
                os.remove('updated.csv')
            df.to_csv('updated.csv')

    # Extract the photos from directory
    def image_from_dir(self, f_path):
        pic = None
        for s_path, s_dirs, s_files in os.walk(f_path):
            try:
                pic = random.choice([os.path.join(s_path, s_file) for s_file in s_files if
                                     os.path.isfile(os.path.join(s_path, s_file))])
            except Exception as e:
                print(e, "Error when choice the pic")
        return pic

    def upload_profile(self, e_data, u_data, exist_data):
        u = instagram(e_data, u_data, exist_data)
        # updated_data = u.edit_profile()
        # self.update_file(updated_data)
        # u.instagramAPI_login()
        # u.post_photo()
        # u.user_following(user_ids=None)
        # u.instabot_login()
        # u.selenium_user_following()
        # u.special_user_following()

    def update_file(self, updated_data):
        if updated_data:
            if os.path.exists('updated.json'):
                with open('updated.json') as f:
                    exist_accounts = json.load(f)
                updated_data = exist_accounts + updated_data

            with open('updated.json', 'w', encoding='utf8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)

def main(event, context):
    u = update_instagram()
    u.update_profile()

if __name__ == "__main__":
    main(0, 0)