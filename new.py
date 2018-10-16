#! python2
# -*- coding: UTF-8 -*-

#coding: UTF-8
#获取帖子列表网页中的每个帖子的链接
#v0.5 python2.7 add https://bt.aisex.com

from bs4 import BeautifulSoup
#import urllib2
import urllib,time,os
import getpagelink, gettorrentlink, gettorrent
import bencode  #解码torrent
from colorama import init,Fore,Back,Style #控制台彩色输出用
import io, sys, re

def refineString(mystring):
    symbol_remove = re.compile("[r'/',r'\',r'?','\u2764','\u3099','\u266a','-$','�$','a>$',u'\xa0']")
    fineString = symbol_remove(' ',mystring)
    symbol_remove = re.compile('\s+')
    fineString = symbol_remove(' ',fineString)
    symbol_remove = re.compile('\s*$')
    fineString = symbol_remove('',fineString)
    fineString.strip()
    
    return fineString
