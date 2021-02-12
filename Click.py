from tkinter import Tk,Frame,Label,Entry,NORMAL
from time import sleep
from pyautogui import moveTo,mouseUp,mouseDown
# GUI界面设置
# 基础设置
root = Tk()
root.title('代刷游戏') #标题
root.geometry('300x200')# 大小
frm = Frame(root)
#提示
label1 = Label(frm,text='提示:坐标点输入格式，\n如200,300;400,300;222,333 \n 每个点之间分号，最后不需要分号，\n坐标之间用逗号，注意用英文键盘\n每个坐标点的测量方法可以用截图工具\n作者：TangHuanqiang')
label1.pack(side='top')
frm.pack(side='top')
def botton():
    positions = enter1.get().split(';')
    stop = int(sleep_time.get())
    while True:
        for position in positions:
            sleep(stop) 
            x= int(position.split(',')[0])
            y= int(position.split(',')[1])
            print(x,y)
            moveTo(x,y)
            mouseDown() # 鼠标左键按下再松开
            sleep(0.2)
            mouseUp()
def get_enter(event):
    botton()
#输入框
frm1 = Frame(root)
frm2 = Frame(frm1)
frm3 = Frame(frm1)

sleep_time = Entry(frm3,state=NORMAL)
sleep_time.bind('<Key-Return>',get_enter)
sleep_time.pack(side='top')
enter1 = Entry(frm3,state=NORMAL)
enter1.bind('<Key-Return>',get_enter)
enter1.pack(side='bottom')
frm3.pack(side='right')
label2 = Label(frm2,text='每次点击间隔时间')
label3 = Label(frm2,text='连续的坐标点')
label2.pack(side='top')
label3.pack(side='bottom')
frm2.pack(side='left')
frm1.pack(side='left')

root.mainloop()