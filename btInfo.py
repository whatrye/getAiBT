#! python3
# -*- coding: UTF-8 -*-

#coding: UTF-8

#module py3-bdecode
from bencode import *

class GetTorrent():
    def getBT(self, file_path):
        with open(file_path, 'rb+') as fp:
            message = bdecode(fp.read())
            return message
    def getMessage(self, message, mode='print'):
        # print(type(message))
        print("发现了一下信息：")
        i_lsit = []
        if mode == 'print':
            for i in message:
                i_lsit.append(i)
                print(i)
        elif mode == 'return':
            return i_lsit
    # 获得tracker数据
    def getannounce(self, message, mode='print'):
        if mode == 'print':
            print("=" * 50, "announce", "=" * 50)
            print("announce的数据类型为:", type(message[b'announce']))
            print("tracker服务器列表：")
            print(message[b'announce'].decode())
        elif mode == 'return':
            return message[b'announce'].decode()
    # 获得备用备用tracker服务器列表
    def getannounce_list(self, message, mode='print'):
        line_lsit = []
        if mode == 'print':
            print("=" * 50, "announce-list", "=" * 50)
            print("announce-list的数据类型为:", type(message[b'announce-list']))
            print("备用tracker服务器列表：")
            for udp_list in message[b'announce-list']:
                for line in udp_list:
                    line_lsit.append(line.decode)
                    print(line.decode())
        elif mode == 'return':
            return line_lsit
    # 获得种子文件的注释
    def getcomment(self, message, mode='print'):
        if mode == 'print':
            print("=" * 50, "comment", "=" * 50)
            print(message[b'comment'].decode())
        elif mode == 'return':
            return message[b'comment'].decode()
    # 获得创建人或创建程序的信息
    def getcreatedby(self, message, mode='print'):
        if mode == 'print':
            print("=" * 50, "created by", "=" * 50)
            print("创建人或创建程序的信息:", message[b'created by'].decode())
        elif mode == 'return':
            return message[b'created by'].decode()
    # 获得编码方式（经测试，有相当一部分的BT种子没有该信息）
    def getencoding(self, message, mode='print'):
        if mode == 'print':
            print("=" * 50, "encoding", "=" * 50)
            print("encoding的类型是:", type(message[b'encoding']))
            print("获得编码方式：", message[b'encoding'].decode())
        elif mode == 'return':
            return message[b'encoding'].decode()
    # 关于下载的文件的信息（包含了文件名，还有是单文件还是多文件）
    def getinfo(self, message):
        # 获得每个文件里面的类容方法
        def getfilename(files_v):
            # 判断值是否为列表
            if isinstance(files_v, list):
                # 历遍列表
                for file_name in files_v:
                    # 如果列表里面的字符串是bytes类型的则转码，否则直接输出
                    if type(file_name) == bytes:
                        return file_name.decode()
                    else:
                        return file_name
            # 当不是列表时，直接输出（一般为int型目前没发现其他类型）
            else:
                return files_v
       print("=" * 50, "info", "=" * 50)
        # print("info的数据类型为:", type(message[b'info']))
        # 历遍所有的keys
        for k in message[b'info'].keys():
            # print("key:", k)
            value = message[b'info'][k]
            # print("value", value)
            # 如果是files
            if k == b'files':
                # 遍历files列表
                print("该BT种子里总共有%d个文件" % len(value))
                v_i = 0
                for v_list_dic in value:
                    # 遍历列表里的字典得到每一个文件
                    print("第%d个文件" % v_i)
                    for files_k, files_v in v_list_dic.items():
                        data = getfilename(files_v)
                        if files_k == b'length':
                            print("文件大小：%0.2f%s" % (data / 1024 / 1024, "MB"))
                        elif files_k == b'path':
                            print("文件名：", data)
                        else:
                            print(files_k, "：", data)
                    v_i += 1;
            # 如果是是文件名：
            elif k == b'name':
                print("文件名:", value.decode())
            # 如果是文件的MD5校验和：
            elif k == b'md5sum  ':
                # print(type(value))
                print("长32个字符的文件的MD5校验和：", value)
            # 文件长度
            elif k == b'length':
                # print(type(value))
                print("文件长度，单位字节：", value / 1024, "KB")
            elif k == b'path':
                # print(type(value))
                print("文件的路径和名字：", value)
            elif k == b'piece length':
                # print(type(value))
                print("每个块的大小:", value / 1024 / 1024, "MB")
            elif k == b'pieces':
                # print(type(value))
                print("每个块的20个字节的SHA1 Hash的值(二进制格式) ：", str(value))
            elif k == b'piece length':
                # print(type(value))
                print("每个块的大小，单位字节：", value, "B")
            # print("value", v)
    # 获得节点主机信息（好多BT种子没有）
    def getnode(self, message, mode='print'):
        if mode == 'print':
            print("=" * 50, "nodes", "=" * 50)
            print("nodes的数据类型为:", type(message[b'nodes']))
            print(message[b'nodes'])
        elif mode == 'return':
            return message[b'nodes']
#代码测试
if __name__ == '__main__':
    # 创建解析对象
    gettorrent = GetTorrent()
    # 解析BT种子
    message = gettorrent.getBT(r"./test.torrent")
    # 将所有方法加入列表
    func_list = [gettorrent.getMessage,
                 gettorrent.getannounce,
                 gettorrent.getannounce_list,
                 gettorrent.getcomment,
                 gettorrent.getcreatedby,
                 gettorrent.getencoding,
                 gettorrent.getinfo,
                 gettorrent.getnode
                 ]
    # 利用循环使用方法
    # 可能有一些信息是没有的，所以引发异常
    for func in func_list:
        try:
            func(message)
        except Exception as e:
            print("异常为：", e)
            continue