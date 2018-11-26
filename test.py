# -*- coding: utf8 -*-
import sys
import Tkinter
import subprocess

root = Tkinter.Tk()

root.title(u"コンバート")
root.geometry("300x300")

# 選択しているものをコンバート。
def CallCmd(event):
    cmd = 'C:/Users/tatuy/Desktop/%s.txt' % select_edit_box.get()
    returncode = subprocess.Popen(cmd, shell=True)
    # test = Tkinter.Label(text=select_edit_box.get())
    # test.pack()

# 選択関連。
select = Tkinter.Label(text=u'選択')
select.pack()

select_edit_box = Tkinter.Entry(width=30)
select_edit_box.insert(Tkinter.END,"")
select_edit_box.pack()

Button = Tkinter.Button(text=u'コンバート')
Button.bind("<Button-1>",CallCmd)
Button.pack()

# # チェックボックス
# CheckBox1 = Tkinter.Checkbutton(text=u"項目1")
# CheckBox1.pack()
# CheckBox2 = Tkinter.Checkbutton(text=u"項目2")
# CheckBox2.pack()
# CheckBox3 = Tkinter.Checkbutton(text=u"項目3")
# CheckBox3.pack()

# # ラジオボタン
# rdo1 = Tkinter.Radiobutton(root, text='項目1')
# rdo1.place(x=40, y=65)
# rdo2 = Tkinter.Radiobutton(root, text='項目2')
# rdo2.place(x=40, y=90)
# rdo3 = Tkinter.Radiobutton(root, text='項目3')
# rdo3.place(x=40, y=115)

root.mainloop()