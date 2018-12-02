# -*- coding: utf8 -*-
import sys
import Tkinter
import subprocess
import threading
import time
from datetime import datetime

__author__ = "oomori"
__version__ = "1.0.0"

def myfunc(cmd):
    returncode = subprocess.call(cmd)

def mythread(cmd_list):
    threadlist = list()
    for thread_num in range(0, len(cmd_list)):
        print thread_num
        thread = threading.Thread(target=myfunc, args=([cmd_list[thread_num]]),name="thread%d" % thread_num)
        threadlist.append(thread)

    for thread in threadlist:
        thread.start()

    for thread in threadlist:
        thread.join()

def main():
    
    print datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    THREAD_NUM = 12
    CMD_NUM = 100
    cmd_list = []
    num = 0

    for i in range(0, CMD_NUM):
        cmd_list.append('python C:/Users/tatuy/Desktop/create.py %d' % (i))

    while num < CMD_NUM:
        list = []
        for i in range(0, THREAD_NUM):
            list_no = num+i
            if(list_no < CMD_NUM):
                print cmd_list[list_no]
                list.append(cmd_list[list_no])
            else:
                break
        mythread(list)
        num += THREAD_NUM

        

    print datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def main2():
    
    print datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    THREAD_NUM = 4
    CMD_NUM = 100
    cmd_list = []
    for i in range(0, CMD_NUM):
        cmd_list.append('python C:/Users/tatuy/Desktop/create.py %d' % (i))
    for thread_num in range(0, 100):
        myfunc(cmd_list[thread_num])

    print datetime.now().strftime("%Y/%m/%d %H:%M:%S")


if __name__ == "__main__":
    main()
    #main2()

    # 0:05:09から0:01:22に短縮 4スレ
    #
