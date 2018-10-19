#! python2
# -*- coding: UTF-8 -*-

#coding: UTF-8
#获取帖子列表网页中的每个帖子的链接
#v0.5 python2.7 add https://bt.aisex.com

import urllib,time,os
from colorama import init,Fore,Back,Style #控制台彩色输出用
import io, sys, re

def removeSstr(mystr):
    #去除特定字符串
    #去除标题尾部的'[vip474]'字串
    sy_beremove = re.compile('\[vi.*?4\]')
    mt_str = sy_beremove.sub('',mystr)

    '''
    pos_vip474 = mystr.find('[vi')
    if pos_vip474 != -1:
        mt_str = mystr[0:pos_vip474]
    else:
        mt_str = mystr
        '''
        
    #去除标题开头的'[MP4/x.xxG]'字串
    mt1_str = re.compile('\[M.*?G\]').sub('',mt_str)

    outstr = re.compile('\[M.*?MB\]').sub('',mt1_str)

    '''
    pos_b = mt_str.find('G]')
    if pos_b != -1:
        mt1_str = mt_str[pos_b+2:]
    else:
        mt1_str = mt_str
        
    pos_c = mt1_str.find('M]')
    if pos_c != -1:
        outstr = mt1_str[pos_c+2:]
    else:
        outstr = mt1_str
        '''
    return outstr

def refineString(mystring):
    #去除特定字符
    symbol_remove = re.compile("[r'/',r'\',r'?',r':']")
    fineString = symbol_remove.sub(' ',mystring)

    symbol_remove = re.compile('-$')
    fineString = symbol_remove.sub(' ',fineString)
    
    symbol_remove = re.compile('�$')
    fineString = symbol_remove.sub(' ',fineString)
    
    symbol_remove = re.compile('a>$')
    fineString = symbol_remove.sub(' ',fineString)
    
    symbol_remove = re.compile("['\u2764','\u3099','\u266a',u'\xa0']")
    fineString = symbol_remove.sub('',fineString)

    symbol_remove = re.compile('\s+')
    fineString = symbol_remove.sub(' ',fineString)

    symbol_remove = re.compile('\s*$')
    fineString = symbol_remove.sub('',fineString)

    fineString.strip()    
    return fineString

if __name__ == '__main__':
    print 'not run in module mode ',__name__
