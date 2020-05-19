#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取网页中的torrent的链接码,应用于jandown这个网站

from bs4 import BeautifulSoup
#import urllib2, urllib
import requests

def get_torrentTittleAndPic(myreq_url='https://bt.aisex.com/bt/htm_data/16/1609/860163.html',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r1 = requests.get(myreq_url,headers = headers, timeout = 15)
    except Exception as e:
        print('error:',e)
        

    soup = BeautifulSoup(r1.content,'html.parser')

    #获取img到列表imgs
    imgs = []
    m_imgs = soup.find('div',id = 'read_tpc').find_all('img')
    for m_img in m_imgs:
        imgs.append(m_img.get('src'))
    return imgs

if __name__ == '__main__':
    print(get_torrentTittleAndPic(myreq_url='https://www.aisex.com/bt/htm_data/16/1609/860163.html'))
