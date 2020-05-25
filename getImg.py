#! python3
# -*- coding: UTF-8 -*-
#coding: UTF-8
#获取torrent的相关图片

from bs4 import BeautifulSoup
import requests,queue,threading

imgQueue = queue.Queue()

def getImg(imgLink='http://www.sinabt.com/B/BxeA7QN6.jpg',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取torrent的相关图片"
    proxies = {}
    timeout = 15
    picFilename = ''
    
    picFilename = imgLink[imgLink.rfind('/')+1:len(imgLink)]

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r1 = requests.get(imgLink, headers = headers,proxies = proxies,timeout = timeout)
        #r1 = requests.get('http://www.jandown.com/fetch.php',params = formdata, headers = headers) #print的结果是b''，不知什么2进制意思，内容是否为空
        content = r1.content
    except Exception as e:
        print('error:',e)
        
    #print
    #print 'The real URL is: '
    #print response.geturl()
    #print
    #print 'The Response info is:'
    #info=response.info()
    #for key,value in info.items():
    #    print "%s = %s" % (key,value)
    #print

    return picFilename,content

def getImgT(myQueue,outpath,enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取torrent的相关图片"
    proxies = {}
    timeout = 15
    picFilename = ''

    imgLink = myQueue.get_nowait()
    picFilename = imgLink[imgLink.rfind('/')+1:len(imgLink)]

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r1 = requests.get(imgLink, headers = headers,proxies = proxies,timeout = timeout)
        imgContent = r1.content
        if len(imgContent) > 0:
            picFullpath = (outpath + r'/' + picFilename)
            ofile = open(picFullpath,'wb')
            ofile.write(imgContent)
            ofile.close()
    except Exception as e:
        print('error:',e)

def getImgs(imgList,outpath):
    for item in imgList:
        imgQueue.put(item)
    threadN = 10
    jqueue = imgQueue.qsize()
    if jqueue < threadN:
        threadN = jqueue

    threads = []
    for i in range(0,threadN):
        thread = threading.Thread(target = getImgT, args = (imgQueue,outpath,))
        threads.append(thread)
        thread.start()
    for thread1 in threads:
        thread1.join()

if __name__ == '__main__':
    outfilename,imgContent = getImg()
    outfile = open(outfilename,'wb')
    outfile.write(imgContent)
    outfile.close()
    print(outfilename,' be saved')
