# -*- coding: utf8 -*-

import os
import sys
import csv
import xlrd
import Tkinter
import subprocess
import threading
import time
from datetime import datetime

def ToCSV(in_file, out_dir):
    # 読み込み。
    book = xlrd.open_workbook(in_file)

    for sheet in book.sheets():
        sheet_name = sheet.name
        dest_path = os.path.join(out_dir, sheet_name + '.csv')
        with open(dest_path, 'w') as fp:
            writer = csv.writer(fp)
            for row in range(sheet.nrows):
                li = []
                for col in range(sheet.ncols):
                    cell = sheet.cell(row, col)
                    if cell.ctype == xlrd.XL_CELL_NUMBER:  # 数値
                        val = cell.value
                        if val.is_integer():
                            # 整数に'.0'が付与されていたのでintにcast
                            val = int(val)
                    else:
                        val = cell.value
                    li.append(val)
                writer.writerow(li)

def myfunc(sheet, out_dir):
    sheet_name = sheet.name
    dest_path = os.path.join(out_dir, sheet_name + '.csv')
    with open(dest_path, 'w') as fp:
        writer = csv.writer(fp)
        for row in range(sheet.nrows):
            li = []
            for col in range(sheet.ncols):
                cell = sheet.cell(row, col)
                if cell.ctype == xlrd.XL_CELL_NUMBER:  # 数値
                    val = cell.value
                    if val.is_integer():
                        # 整数に'.0'が付与されていたのでintにcast
                        val = int(val)
                else:
                    val = cell.value
                li.append(val)
            writer.writerow(li)

def mythread(cmd_list):
    threadlist = list()
    for thread_num in range(0, len(cmd_list)):
        print thread_num
        thread = threading.Thread(target=myfunc, args=([cmd_list[thread_num],out_dir]),name="thread%d" % thread_num)
        threadlist.append(thread)

    for thread in threadlist:
        thread.start()

    for thread in threadlist:
        thread.join()


def ToCSVMult(in_file, out_dir, thread_num):
    # 読み込み。
    book = xlrd.open_workbook(in_file)

    THREAD_NUM = thread_num
    sheet_num = len(book.sheets())
    num = 0

    while num < sheet_num:
        list = []
        for i in range(0, THREAD_NUM):
            list_no = num+i
            if(list_no < sheet_num):
                sheet = book.sheets()[i]
                print sheet
                list.append(sheet)
            else:
                break
        mythread(list)
        num += THREAD_NUM

def res_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

print datetime.now().strftime("%Y/%m/%d %H:%M:%S")

is_mult = sys.argv[1]

is_exists = False

if len(sys.argv) == 2:
    print u"エクセルファイルが設定されていません。\n"
else:
    is_exists = os.path.exists(sys.argv[2])
    if is_exists is False:
        print u"ファイルが存在しません。出力ファイルから設定してください。\n"
    in_file = sys.argv[2]

if is_exists is True:

    if len(sys.argv) == 4:
        out_dir = sys.argv[3]
    elif len(sys.argv) == 3:
        print u"出力パスが設定されていません。現在実行中のパスで出力します。"
        out_dir = ""

    if is_mult == "1":
        print u"シングル！"
        ToCSV(in_file, out_dir)
        
    else:
        print u"マルチ！"
        thread_num = int(res_cmd("set NUMBER_OF_PROCESSORS").split("=")[1])
        ToCSVMult(in_file, out_dir, thread_num)
        

    print datetime.now().strftime("%Y/%m/%d %H:%M:%S")