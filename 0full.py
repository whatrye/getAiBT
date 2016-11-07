#coding: utf-8
#获取帖子列表网页中的每个帖子的链接

from bs4 import BeautifulSoup
import urllib2,urllib,time,os
import getpagelink, gettorrentlink, gettorrent
import bencode
#调用时使用gettorrent.get_torrent()
#或者 from getpagelink import *
#from gettorrentlink import *
#from gettorrent import *
#调用时直接使用 get_torrent

#test code block
#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent','Mozilla/5.0')]
#print opener.open('http://www.xici.net').read()

torrentsPath = 'torrents'
if not os.path.exists(torrentsPath):
    os.makedirs(torrentsPath)

enable_proxy = False
if enable_proxy:
    print 'proxy enabled\n'
    
user_agent = 'Mozilla/5.0'
mypage_number = 1
total_pages = 2
pagelink_pre ='http://208.94.244.98/bt/thread.php?fid=16&page='
link_dict = {}
#link_dict[1] = getpagelink.getlink_list(my_page = myfirst_page)
for mypage_number in range(1,total_pages+1):
    cur_page = pagelink_pre + str(mypage_number)
    link_dict[mypage_number] = getpagelink.getlink_list(my_page = cur_page, enable_proxy = enable_proxy)
print 'link_dict length is: '+str(len(link_dict))

n = 0
link_nu = 1
for link_nu in range(1,len(link_dict)+1):
    for link,name in link_dict[link_nu].items():
        n=n+1
        print n,unicode(link),unicode(name)

        outfile_name = unicode(name+'.torrent')
        outfile_full_path = unicode(torrentsPath+'\\'+outfile_name)
        
        if os.path.exists(outfile_full_path) and os.path.isfile(outfile_full_path) and os.access(outfile_full_path,os.R_OK):
            print 'this torrent file already exist, skip save.\n'
        else:
            #获取torrent代码
            torrent_code = gettorrentlink.get_torrentlink(myreq_url = link, enable_proxy = enable_proxy)
            print torrent_code
            
            #获取torrent内容
            torrent_content = gettorrent.get_torrent(torrent_name_code = torrent_code, enable_proxy = enable_proxy)
            #print torrent_content
            #print
            
            try:
                btinfo = bencode.bdecode(torrent_content)
            except Exception,detail:
                print "ERROR: ",detail
                print
                continue
                
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
            print '%d files'%len(btlist)
            #print 'the MAX file in the torrent %s is: '%outfile_name + unicode(temppath)
            print 'the MAX file in the torrent is: ', unicode(temppath)
            print 'size : ',  str(temp), '\n'
            
            #输出torrent文件
            #print 'file not exist\n'+ outfile_full_path
            outFile = open(outfile_full_path,'wb')
            outFile.write(torrent_content)
            outFile.close()
            time.sleep(1)

print
print 'over'
