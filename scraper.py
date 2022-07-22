import sys
import requests
from bs4 import BeautifulSoup
from PIL import Image
import helpers

accepted_args = ['-berserk', '-chainsaw_man', '-h']
arg = sys.argv[1]

if arg not in accepted_args:
    print('did not give accepted args. accepted args are: ')
    print(accepted_args)
elif arg == '-h':
    print('available args: ')
    print(accepted_args)
else:
    # building all urls
    urls = []
    if arg == "-berserk":
        urls = helpers.build_urls_for_berserk()
    elif arg == "-chainsaw_man":
        urls = helpers.build_urls_for_chainsaw_man()

    # for every url provided, download every image
    all_downloaded_img_names = helpers.download_all_imgs_from_all_urls(urls)

    # convert all images into 1 pdf
    image_1 = Image.open(all_downloaded_img_names[0])
    img_1 = image_1.convert('RGB')
    img_list_for_pdf = []

    for img_name in all_downloaded_img_names[1:]:
        a = Image.open(img_name)
        b = a.convert('RGB')
        img_list_for_pdf.append(b)

    img_1.save('chaps.pdf', save_all=True, append_images=img_list_for_pdf)
    print('saved pdf')