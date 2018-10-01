#coding: UTF-8
#获取帖子列表网页中的每个帖子的链接
#v0.5 python2.7 add https://bt.aisex.com

from bs4 import BeautifulSoup
import urllib2,urllib,time,os
import getpagelink, gettorrentlink, gettorrent
import bencode  #解码torrent
from colorama import init,Fore,Back,Style #控制台彩色输出用
import io, sys

def main():
    print (u'系统默认编码：',sys.getdefaultencoding()) #获取系统默认编码
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码

    init(autoreset = True)

    #调用时使用gettorrent.get_torrent()
    #或者 from getpagelink import *
    #from gettorrentlink import *
    #from gettorrent import *
    #调用时直接使用 get_torrent

    torrentsPath = 'torrents'
    if not os.path.exists(torrentsPath):
        os.makedirs(torrentsPath)

    enable_proxy = False
    if enable_proxy:
        print('proxy enabled\n\n')
    else:
        print ('proxy disabled\n\n')
    '''
    if enable_proxy:
        print(Fore.GREEN + 'proxy enabled\n\n')
    else:
        print (Fore.GREEN + 'proxy disabled\n\n')
    '''    
    proxy_string = {"http":"127.0.0.1:8787","https":"127.0.0.1:8787","socks":"127.0.0.1:1080"}
    user_agent = 'Mozilla/5.0'

    if len(sys.argv) > 1:
        firstpage_number = int(sys.argv[1])
        total_pages = int(sys.argv[2])
    else:
        firstpage_number = 1
        total_pages = 2
    #page_host = u'www.aisex.com'
    #pagelink_pre = u'https://' + page_host + u'/bt/thread.php?fid=16&page='
    #pagelink_pre ='https://www.aisex/bt/thread.php?fid=16&page='
    page_host = u'bt.aisex.com'
    pagelink_pre = u'https://' + page_host + u'/bt/thread.php?fid=16&page='
    link_dict = {}
    #link_dict[1] = getpagelink.getlink_list(my_page = myfirst_page)
    link_count = 0
    for mypage_number in range(firstpage_number,firstpage_number+total_pages):
        cur_page = pagelink_pre + str(mypage_number)
        link_dict[mypage_number] = getpagelink.getlink_list(my_page = cur_page, page_host = page_host, enable_proxy = enable_proxy, proxy_string = proxy_string)
        link_count = link_count + len(link_dict[mypage_number])
    print ('link_dict length is: '+str(len(link_dict)) + '\n')
    print ('Total links: ', link_count, '\n')
    '''
    print (Fore.YELLOW + 'link_dict length is: '+str(len(link_dict)) + '\n')
    print (Fore.CYAN + 'Total links: ', link_count, '\n')
    '''

    n = 0
    link_nu = 1
    for link_nu in range(firstpage_number,firstpage_number+len(link_dict)):
        print (link_nu)
        for link,name in link_dict[link_nu].items():
            n = n+1
            print (n,unicode(link))
            #print u'name 的编码形式: ',name.__class__ #获取name的编码形式
            print ('     ' + name.encode('gb18030'))  #文件名输出有编码问题

            outfile_name = unicode(name+'.torrent')
            outfile_full_path = unicode(torrentsPath+'\\'+outfile_name)
            
            if os.path.exists(outfile_full_path) and os.path.isfile(outfile_full_path) and os.access(outfile_full_path,os.R_OK):
                print ('this torrent file already exist, skip save.\n')
                #print Fore.RED + Style.BRIGHT + 'this torrent file already exist, skip save.\n'
            else:
                #获取torrent代码
                torrent_code = gettorrentlink.get_torrentlink(myreq_url = link, enable_proxy = enable_proxy, proxy_string = proxy_string)
                print ('     ' + torrent_code)
                #print '     ' + Fore.BLUE + Back.YELLOW + torrent_code
                
                #获取torrent内容
                torrent_content = gettorrent.get_torrent(torrent_name_code = torrent_code, enable_proxy = enable_proxy, proxy_string = proxy_string)
                #print torrent_content
                #print
                
                #解码torrent
                try:
                    btinfo = bencode.bdecode(torrent_content)
                except (Exception,detail):
                    print ("     ERROR4: ",detail)
                    print   ()
                    continue
                print ('     decode torrent finished')
                    
                info = btinfo['info']
                btlist = {}
                for ls in info['files']:
                    if len(ls['path']) > 1:
                        btlist[ls['path'][0]] = {'path':ls['path'][0]+'/'+ls['path'][1],'size':ls['length']}
                        #print btlist[ls['path'][0]]
                    else:
                        btlist[ls['path'][0]] = {'path':ls['path'][0],'size':ls['length']} #生成新字典{path:{'path':path,'size':size}}
                        #print "file name: " + btlist[ls['path'][0]]['path'].decode('utf-8')
                        #print 'size: '+unicode(btlist[ls['path'][0]]['size'])
                temp = 0
                for key,val in btlist.items():
                    if val['size'] > temp:
                        temp = val['size']
                        temppath = val['path']
                print ('     %d files'%len(btlist))
                try:
                    print ('     the MAX file in the torrent %s is: '%outfile_name + unicode(temppath))
                except (Exception, detail):
                    print ('     Error5: ',detail)
                #print 'the MAX file in the torrent is: ', temppath.decode('gbk')
                #print 'size : ',  str(temp), '\n'
                
                #输出torrent文件
                #print 'file not exist\n'+ outfile_full_path
                outFile = open(outfile_full_path,'wb')
                outFile.write(torrent_content)
                outFile.close()
                #time.sleep(1)

    print   ()
    print ('over')

if __name__ == '__main__':
    print (__name__)
    main()

