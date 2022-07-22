import requests
import shutil
from bs4 import BeautifulSoup
from PIL import Image

# for a given list of urls, download every image from every url
# returns list of all downloaded image file names
def download_all_imgs_from_all_urls(urls):
    all_downloaded_img_names = []

    for url in urls:
        # get raw html and setup soup to parse
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        all_imgs = soup.findAll('img')

        # get all img urls and download all images
        all_img_urls = list(map(lambda x: x['src'], all_imgs))
        all_downloaded_img_names.extend(download_imgs_from_img_urls(all_img_urls))

    return all_downloaded_img_names

# downloads all images from given img urls
# returns list of image file names
def download_imgs_from_img_urls(img_urls):
    img_names = []
    img_urls = sanitized_img_urls(img_urls)

    for img_url in img_urls:
        fn = img_url.split("/")[-1]
        # spoof headers
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
        r = requests.get(img_url, headers=headers, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True

            with open(fn, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
                img_names.append(f.name)

            print('successfully downloaded')
        else:
            print(f'image not retrieved properly, status code: {r.status_code}, {r.url}')

    return img_names

# need to sanitize img urls because some sites have escaped chars in their links -_-, particularly chainsaw man
def sanitized_img_urls(img_urls):
    sanitized = []
    for img_url in img_urls:
        if img_url.endswith("\r"):
            sanitized.append(img_url[:-1])
        else:
            sanitized.append(img_url)
    return sanitized

# berserk url used uses 001 -> 300 style of numbering
def build_urls_for_berserk():
    # build custom chapter numbers
    chap_nums = []
    latest_chap = 20
    for num in range(1, latest_chap + 1):
        num_to_chap_str = ""
        if num < 10:
            num_to_chap_str = f'00{num}'
        elif num < 100:
            num_to_chap_str = f'0{num}'
        else:
            num_to_chap_str = f'{num}'
        chap_nums.append(num_to_chap_str)

    # building all urls
    urls = []
    for chap_num in chap_nums:
        urls.append(f'https://readberserk.com/chapter/berserk-chapter-{chap_num}/')

    return urls

# chainsaw man url used uses 1 -> 99 style of numbering
def build_urls_for_chainsaw_man():
    # no need to build custom chap nums like berserk
    # building all urls
    latest_chap = 1
    urls = []
    for i in range(1, latest_chap + 1):
        urls.append(f'https://ww2.readchainsawman.com/chapter/chainsaw-man-chapter-{i}/')

    return urls