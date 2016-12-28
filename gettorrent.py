#coding: utf-8
#获取www.jandown.com上的torrent

from bs4 import BeautifulSoup
import urllib2,urllib

def get_torrent(torrent_name_code='9XAlbQ2DCd',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "获取torrent的实际内容"
    user_agent='Mozilla/5.0'
    formdata={'code':torrent_name_code}
    data_encoded=urllib.urlencode(formdata)
    #这样也行
    #data_encoded=urllib.urlencode([('code','9XAlbQ2DCd')])

    myheaders={'User-Agent':user_agent}
    #enable_proxy = False

    #可以通过下面的方法把Debug Log打开，这样收发包的内容就会在屏幕上打印出来，
    #方便我们调试，在一定程度上可以省去抓包的工作。
    #httpHandler =urllib2.HTTPHandler(debuglevel=1)
    #httpsHandler =urllib2.HTTPSHandler(debuglevel=1)
    #opener =urllib2.build_opener(httpHandler, httpsHandler)
    #urllib2.install_opener(opener)

    print '     Fetching Torrent file ...'
    try:
    #使用proxy的添加。build_opener用于自定义Opener对象，应用于验证(HTTPBasicAuthHandler)、cookie(HTTPCookieProcessor)、代理(ProxyHandler)
    #在程序中明确控制Proxy而不是受环境变量http_proxy的影响
        proxy_handler=urllib2.ProxyHandler(proxy_string)
        null_proxy_handler=urllib2.ProxyHandler({})
        if enable_proxy:
            opener=urllib2.build_opener(proxy_handler)
        else:
            opener=urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)


    #这样也行,url,data,headers也都可以一起放在Request里，然后直接urlopen(req)
    #    opener.addheaders = [('User-agent','Mozilla/5.0')]
    #    urllib2.install_opener(opener)
    #    req=urllib2.Request('http://www.jandown.com/fetch.php')
    #    response=urllib2.urlopen(req,data_encoded)
        
    #install_opener可要可不要
    #    urllib2.install_opener(opener)
    #Request中带data的自动变为POST方法，否则为GET方法，或者data放在urlopen里也一样
    #如果你不创建一个Request,而是直接使用urlopen()方法,Python强制把Content-Type改为application/x-www-form-urlencoded.
        req=urllib2.Request(url='http://www.jandown.com/fetch.php',data=data_encoded,headers=myheaders)
        response=urllib2.urlopen(req)
        content=response.read()
        #print
        #print 'The real URL is: '
        #print response.geturl()
        #print
        #print 'The Response info is:'
        #info=response.info()
        #for key,value in info.items():
        #    print "%s = %s" % (key,value)
        #print

    except urllib2.HTTPError, e:
        print "     ERROR: Code",e.code
    except Exception,detail:
        print "     ERROR: ",detail

    return content

if __name__ == '__main__':
    get_torrent()
#outFile = open('out.torrent','wb')
#torrent_content=get_torrent()
#outFile.write(torrent_content)
#outFile.close()
