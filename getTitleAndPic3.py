#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取网页中的图片链接和网页标题

from bs4 import BeautifulSoup
import requests

def get_torrentTitleAndPic(myreq_url='https://bt.aisex.com/bt/htm_data/16/1609/860163.html',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r1 = requests.get(myreq_url,headers = headers, timeout = 15)
    except Exception as e:
        print('error:',e)
        

    soup = BeautifulSoup(r1.content,'html.parser')

    #获取img链接到列表imgs
    imgs = []
    m_imgs = soup.find('div',id = 'read_tpc').find_all('img')
    for m_img in m_imgs:
        imgs.append(m_img.get('src'))

    #获取title
    title = ''
    title = soup.find('h1',id = 'subject_tpc').next_element #或者.get_text() 或者.text 或者.innerHTML 或者.innerText
    title = title.strip()
##    print(title)
    return title,imgs

if __name__ == '__main__':
    print(get_torrentTitleAndPic(myreq_url='https://bt.aisex.com/bt/htm_data/16/2005/1022016.html'))
