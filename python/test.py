# -*- coding: utf8 -*-
import sys
import Tkinter
import subprocess

root = Tkinter.Tk()

root.title(u"コンバート")
root.geometry("300x300")

# 選択しているものをコンバート。
def CallCmd(event):
    cmd = 'python to_csv.py' % select_edit_box.get()
    returncode = subprocess.Popen(cmd, shell=True)
    # test = Tkinter.Label(text=select_edit_box.get())
    # test.pack()

# 選択関連。
select = Tkinter.Label(text=u'エクセルファイル選択')
select.pack()

select_edit_box = Tkinter.Entry(width=30)
select_edit_box.insert(Tkinter.END,"")
select_edit_box.pack()

# 出力関連。
out = Tkinter.Label(text=u'出力パス設定')
out.pack()

out_edit_box = Tkinter.Entry(width=30)
out_edit_box.insert(Tkinter.END,"")
out_edit_box.pack()

Button = Tkinter.Button(text=u'コンバート')
Button.bind("<Button-1>",CallCmd)
Button.pack()

# チェック有無変数
var = Tkinter.IntVar()
# value=0のラジオボタンにチェックを入れる
var.set(0)

# ラジオボタン
rdo1 = Tkinter.Radiobutton(root, value=0, variable=var, text='シングル')
rdo1.place(x=60, y=100)
rdo2 = Tkinter.Radiobutton(root, value=1, variable=var, text='マルチ')
rdo2.place(x=60, y=120)

root.mainloop()