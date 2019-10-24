import requests
from lxml import html
from PIL import Image
import urllib
url = "https://www.google.com/search?q=resort+images&tbm=isch&source=univ&sa=X&ved=2ahUKEwiu8-SU3sPkAhWInp4KHTMvChAQsAR6BAgHEAE"
url = "https://www.google.com/search?q=australia+resort+images&tbm=isch&source=lnt&tbs=isz:l&sa=X&ved=0ahUKEwiJv-zWgcTkAhWpT98KHTzBAT0QpwUIIg&biw=1920&bih=888&dpr=1"
base_url = 'D:\\Work\\instagram_script\\post_photos'
size_list = {}
size_list['medium_size'] = [300, 153]
size_list['large_size'] = [1024, 521]
try:
    resp = requests.get(url)
    if resp.status_code == 200:
        tree_html = html.fromstring(resp.text)
        images = tree_html.xpath("//img/@src")
        for image in images:
            img = Image.open(urllib.request.urlopen(image))
            img_format = img.format
            resized_img = img.thumbnail((300, 170))
            print(str(img.size))
            # resized_img = im.resize((size_list['large_size'][0], size_list['large_size'][1]), Image.ANTIALIAS)
            if img and (img_format.lower() == 'jpeg' or img_format.lower() == 'png'):
                img_name = image[-5:]
                image_path = base_url + '\\' + img_name + '.jpg'
                img.save(image_path + '.jpg')
                # im.save(image_path + '.jpg')
except Exception as e:
    print(e)
