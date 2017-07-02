#-*- coding:utf-8 -*-

from urllib.request import urlopen 
from bs4 import BeautifulSoup as BS
import os
import time
import multiprocessing
import requests

def get_page(url):
    html = BS(urlopen(url))
    page_num = str(html.find("span","current-comment-page"))[36:39]

    return page_num



def find_imgs(url):
    html = BS(urlopen(url))
    imgs_addrs = []
    for link in html.find_all('a',"view_img_link"):
        imgs_addrs.append('http:'+link.get('href'))
        # print(link.get('href'))

    return imgs_addrs

def get_image(url):
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'

            }
    r = requests.get(url,headers = headers)
    return r.content

def save_imgs(folder,img_addrs):
    for img_link in img_addrs:
        print(img_link)
        filename = img_link.split('/')[-1]
        with open(filename,'wb') as f:
            imgData = get_image(img_link)
            f.write(imgData)
        # time.sleep(3)


def get_pic(last_page,page_url,now_folder) :
    print(page_url)
#写入最新page
    with open('lastpage.txt', 'w') as f:
        f.write(str(last_page))
    folder = str(last_page)
    if os.path.exists("folder") == 1:
        pass
    else:
        os.mkdir(folder)
        os.chdir(folder)
        img_addrs = find_imgs(page_url)
        save_imgs(folder,img_addrs)
        os.chdir(now_folder)

def jiandan_pic_download():

#判断lastpage.txt是否存在    
    if os.path.exists("lastpage.txt") == 1:
        pass
    else :
        with open('lastpage.txt', 'w') as f:
            f.write('1')  
#读取上次下载页数
    with open('lastpage.txt', 'r') as f:
        last_page = int(f.readline())
#获得当前最新page
    url = 'http://jandan.net/ooxx/'
    page_num = int(get_page(url))
    #print(page_num)
    pages = page_num - last_page

#    folder = str(page_num)+"-"+ time.strftime("%y%m%d",time.localtime())
#    os.mkdir(folder)
#    os.chdir(folder)

    now_folder = os.getcwd()
    
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(pages):    
        page_url = url + 'page-' + str(last_page) +'#comments'
        pool.apply_async(get_pic, (last_page,page_url,now_folder ))
        os.chdir(now_folder)
        last_page += 1
    pool.close()
    pool.join()
    
    print("大爷,没有妹子啦!下次再来吧!")
if __name__ == '__main__':
    jiandan_pic_download()
