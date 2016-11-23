#coding: UTF-8
#获取帖子列表网页中的每个帖子的链接

from bs4 import BeautifulSoup
import urllib2,urllib
import re
pattern = re.compile("[.*M]")
pattern2 = re.compile("[.*G]")

def getlink_list(my_page='http://208.94.244.98/bt/thread.php?fid=16&page=2',enable_proxy = False):
    "获取网页中帖子链接的列表"
    user_agent='Mozilla/5.0'
    mypre_link=u'http://208.94.244.98/bt/'

    myheaders = {'User-Agent':user_agent}
    #enable_proxy = False

    try:
    #使用proxy的添加。build_opener用于自定义Opener对象，应用于验证(HTTPBasicAuthHandler)、cookie(HTTPCookieProcessor)、代理(ProxyHandler)
    #在程序中明确控制Proxy而不是受环境变量http_proxy的影响
        proxy_handler=urllib2.ProxyHandler({"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"})
        null_proxy_handler=urllib2.ProxyHandler({})
        if enable_proxy:
            opener=urllib2.build_opener(proxy_handler)
        else:
            opener=urllib2.build_opener(null_proxy_handler)
        urllib2.install_opener(opener)

        req=urllib2.Request(url=my_page,headers=myheaders)
        response=urllib2.urlopen(req)
        content=response.read()
        content = content.decode("gbk","ignore")
        if isinstance(content,unicode):
            print 'the content is unicode\n'
        else:
            print 'the content is not unicode\n'
        print content.__class__
#        print
#        print 'The real URL is: '
#        print response.geturl()
#        print
#        print 'The Response info is:'
#        info=response.info()
#        for key,value in info.items():
#            print "%s = %s" % (key,value)
#        print
#        print 'Here is the content:'
#        print content
#        print

        #outFile.write(content)
        soup = BeautifulSoup(content,'html.parser')
        mytags_a=soup.find_all('a')
        #print 'A tags-----------'
        link_list=[]
        link_dict={}
        n = 0
        for mytag_a in mytags_a:
            mytag_href = str(mytag_a.get('href'))
            mytag_title = mytag_a.get('title')
            mytag_string = mytag_a.string
            #mytag_string = mytag_string.decode('gbk') #将GBK编码转换为unicode，如果要把unicode转为gbk则用encode('gbk')
            #也可用unicode(str,'gbk'),与str.decode('gbk')一样
            if mytag_href.find('htm_data') != -1:
                if mytag_title == None:
                    if mytag_string.find(u'发帖者')==-1 & mytag_string.find(u'版规')==-1:            
                        #print 'the tag A is: %s' %unicode(mytag_a)
                        #print 'the href is: %s' %unicode(mytag_href)
                        myfull_link=mypre_link+mytag_href
                        link_list.append(myfull_link)
                        
                        #去除标题尾部的'[vip474]'字串
                        pos_vip474 = mytag_string.find('[vi')
                        if pos_vip474 != -1:
                            #print 'is vip474'
                            mt_str = mytag_string[0:pos_vip474]
                        else:
                            #print 'vip474 does not exist'
                            mt_str = mytag_string
                        #去除标题开头的'[MP4/x.xxG]'字串
                        pos_b = mt_str.find('G]')
                        if pos_b !=-1:
                            mt1_str=mt_str[pos_b+2:]
                        else:
                            mt1_str=mt_str
                            
                        pos_c = mt_str.find('M]')
                        if pos_c !=-1:
                            mytorrent_filename=mt1_str[pos_c+2:]
                        else:
                            mytorrent_filename=mt1_str
                        #mytorrent_filename=mytorrent_filename.decode('gbk','ignore')

                        #测试是否是unicode
                        if isinstance(mytorrent_filename,unicode):
                            print 'filename is unicode\n',mytorrent_filename
                        else:
                            print 'filename is not unicode\n',mytorrent_filename
                            print mytorrent_filename.__class__
                            mytorrent_filename = mytorrent_filename.decode('gbk','ignore')
                        print mytorrent_filename.__class__
                            
                        #去除文件名中的空格,"/","\"等字符
                        str_beremove = re.compile(r'["/","\"]')
                        mytorrent_filename = str_beremove.sub('',mytorrent_filename)
                        #去除2个以上的空格
                        str_beremove = re.compile('\s+') #1以及以上的空格，也可以用'\s{2,}'，表示2以及以上的空格
                        mytorrent_filename = str_beremove.sub(' ',mytorrent_filename)
                        #mytorrent_filename.split()
                        #mytorrent_filename = ' '.join(mytorrent_filename.split())
                        #去除尾部"-"号
                        str_beremove = re.compile('-$')
                        mytorrent_filename = str_beremove.sub('',mytorrent_filename)

                        mytorrent_filename.strip()
                        print 'aaaaaaa'
                        print mytorrent_filename	#编码问题老出错
                        print mytorrent_filename.__class__
						
                        
                        #用replace方法去除字符
                        #mytorrent_filename.replace(' ','') #去除文件名中的空格
                        #mytorrent_filename.replace('/','') #去除文件名中的"/"
                        #mytorrent_filename.replace('\\','') #去除文件名中的"\"
                        
                        link_dict[myfull_link]=mytorrent_filename #以赋值的方式生成字典{myfull_link:mytorrent_filename}
                        #print 'the full link is: ', %myfull_link
                        #print 'the A string is: ',  %unicode(mytag_string)
                        #print 'the title of A is: ', %unicode(mytag_title)
                        #print
                        n = n+1
            #linkpos=mylinks[0].string.find('=')
            #print linkpos
            #print mylinks[0].string[linkpos+1:linkpos+11]
        print 'total %s links in this page: %s\n' %(n,my_page)
        #for llink,llname in link_dict.items():
         #   print llink, llname
        #print link_dict

    except urllib2.HTTPError, e:
        print "ERROR: Code",e.code
    except Exception,detail:
        print "ERROR: ",detail

    return link_dict

if __name__ == '__main__':
    print __name__
    for a,b in getlink_list(enable_proxy = True).items():
        print a,b
