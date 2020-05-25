#!python3
# -*- coding: UTF-8 -*-

import requests
import threading
import queue,re,sys,time,os

myqueue = queue.Queue()
def threadFunc(myQueue,para2):
    try:
        val1 = myQueue,get_nowait()
        j = myQueue.qsize()
    except Exception as e:
        break
    return val1

def main():
    for item in bbbb:
        c = item.strip().split(" ")
        myqueue.put(c[0])
    jqueue = myqueue.qsize()

    threadN = 10
    if jqueue < 10:
        threadN = jqueue

    threads = []
    for i in range(0,threadN):
        thread = threading.Thread(target = threadFunc, args = (myqueue,para2,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
