#coding: utf-8
#获取网页中的torrent的链接码

from bs4 import BeautifulSoup
import urllib2, urllib

def get_torrentlink(myreq_url='http://208.94.244.98/bt/htm_data/16/1609/860163.html',enable_proxy = False, proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}):
    "从指定的网页中获取torrent的代码"
    user_agent = 'Mozilla/5.0'
    myheaders = {'User-Agent':user_agent}
    #enable_proxy = False
    torrent_name_code = ''

    try:
    #使用proxy的添加。build_opener用于自定义Opener对象，应用于验证(HTTPBasicAuthHandler)、cookie(HTTPCookieProcessor)、代理(ProxyHandler)
    #在程序中明确控制Proxy而不是受环境变量http_proxy的影响
        proxy_handler = urllib2.ProxyHandler(proxy_string)
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)

        req = urllib2.Request(url = myreq_url, headers=myheaders)
        response = urllib2.urlopen(req)
        content = response.read()

        soup = BeautifulSoup(content,'html.parser')

        #锚点A没被放在img标签里的
        m_as = soup.find('div',id = 'read_tpc').find_all('a') #链接在read_tpc这个div里
        for m_a in m_as:
            #print m_a
            temp_href = m_a.get('href') #这个是获取<a href=...>的href值
            #print temp_href
            pos_jandown = temp_href.find('jandown') #判断是否是包含torrent代码的链接
            #print pos_jandown
            if pos_jandown != -1:
                #print m_a
                #print temp_href
                #print pos_jandown
                linkpos=temp_href.find('=') #需要的torrent代码在"link.php?ref="后面
                #链接码的长度是10
                torrent_name_code = temp_href[linkpos+1:linkpos+11]
        #m_brs = soup.find('div',id='read_tpc').find_all('br')
        #m_br = m_brs[0]
        #print m_br
            
        
        #锚点A被放在了img标签里的
#        myimgs=soup.find('div',id='read_tpc').find_all('img')
        #print 'images-----------'
#        for myimg in myimgs[1:]:
            #print myimg
            #print
#            mylinks = myimg.find_all('a')
#            print u'mylink,href值'
#            myhref = mylinks[0].get('href')    #这个是输出<a href>的href值
#            print myhref
#            print 'A string------'
#            print mylinks[0].string #这个是输出<a>...</a>之间的内容
    #        for mylink in mylinks:
    #            print mylink.string
#            print        
#            linkpos=myhref.find('=') #需要的torrent代码在"link.php?ref="后面
            #linkpos=mylinks[0].string.find('=')
            #或者string.index('=')
#            print linkpos
            #链接码的长度是10
#            torrent_name_code = mylinks[0].string[linkpos+1:linkpos+11]
#            print torrent_name_code

    except urllib2.HTTPError, e:
        print "     ERROR: Code",e.code
    except Exception,detail:
        print "     ERROR: ",detail

    return torrent_name_code

if __name__ == '__main__':
    print get_torrentlink(myreq_url='http://208.94.244.98/bt/htm_data/16/1609/860163.html')
