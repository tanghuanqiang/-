import threading
import time
from tkinter import Tk,Frame,Label,Entry,NORMAL,Button,Text,END,INSERT

from time import sleep
from pyautogui import moveTo,mouseUp,mouseDown,position
# GUI界面设置
# 基础设置

class Gui:
    def __init__(self):
        '''初始化'''
        self.root = Tk()
        self.root.title('自动连点')
        self.root.geometry("960x540")
        self.interface() # 画图
        #获取实时位置线程标志位
        self.getDataThread = None
        self.__getDataFlag = threading.Event()  # 用于暂停线程的标识
        self.__getDataFlag.set()  # 设置为True
        self.__getDataRunning = threading.Event()  # 用于停止线程的标识
        self.__getDataRunning.set()  # 将running设置为True
        # 自动点击线程标志位
        self.startEnterThread = None
        self.__startEnterFlag = threading.Event()  # 用于暂停线程的标识
        self.__startEnterFlag.set()  # 设置为True
        self.__startEnterRunning = threading.Event()  # 用于停止线程的标识
        self.__startEnterRunning.set()  # 将running设置为True




    def interface(self):
        """"界面编写位置"""
        frm = Frame(self.root)
        # 提示
        label1 = Label(frm,text='提示:坐标点输入格式，如200,300;400,300;222,333 \n 每个点之间分号，最后不需要分号，坐标之间用逗号，注意用英文键盘\n每个点位点击并弹开耗时至少0.2s\n作者：DomTang')
        label1.pack(side='top')
        frm.pack(side='top')

        frm1 = Frame(self.root) #输入的位置
        frm2 = Frame(frm1)  #输入提示
        frm3 = Frame(frm1)  #输入框
        frm4 = Frame(frm1)
        frm5 = Frame(self.root)  # 查看实时位置
        # 开始点击的按钮
        self.start = Button(frm4, text="开始自动点击", command=self.start_enter)
        self.start.pack(side='right')
        frm4.pack(side='right')


        #获取时间
        self.sleep_time = Entry(frm3, state=NORMAL)
        #self.sleep_time.bind('<Key-Return>', self.get_enter)
        self.sleep_time.pack(side='top')
        #获取点位
        self.enter1 = Entry(frm3, state=NORMAL)
        #self.enter1.bind('<Key-Return>', self.get_enter)
        self.enter1.pack(side='bottom')
        frm3.pack(side='right')


        #文字提示
        label2 = Label(frm2, text='每次点击间隔时间')
        label3 = Label(frm2, text='连续的坐标点')
        label2.pack(side='top')
        label3.pack(side='bottom')
        frm2.pack(side='left')
        frm1.pack(side='left')

        # 获取实时点位
        self.dataGet = Text(frm5,width=20,height=2)
        self.dataGet.pack(side='left')
        self.bottonGet = Button(frm5, text="获取实时点位",command=self.start_getdata)
        self.bottonGet.pack(side='bottom')
        frm5.pack(side='right')
    def botton(self):
        positions = self.enter1.get().split(';')
        print(self.sleep_time.get())
        stop = float(self.sleep_time.get())


        while self.__startEnterRunning.isSet():

            for position in positions:
                self.__startEnterFlag.wait()
                sleep(stop)
                x = int(position.split(',')[0])
                y = int(position.split(',')[1])
                print(x, y,time.time())
                moveTo(x, y)
                mouseDown()  # 鼠标左键按下再松开
                sleep(0.2)
                mouseUp()
    def start_enter(self):
        if (self.startEnterThread):
            if (self.__startEnterFlag.isSet()):
                self.__startEnterFlag.clear()  # 暂停
            else:

                #重新开始
                del self.startEnterThread
                self.__startEnterFlag.set()  # 恢复
                self.startEnterThread = threading.Thread(target=self.botton)
                self.startEnterThread.setDaemon(True)
                self.startEnterThread.start()
        else:
            self.startEnterThread = threading.Thread(target=self.botton)
            self.startEnterThread.setDaemon(True)
            self.startEnterThread.start()
    def get_data(self):
        '''查看鼠标实时定位具体函数'''

        while self.__getDataRunning.isSet():
            self.__getDataFlag.wait()
            # todo
            time.sleep(0.008)
            self.dataGet.delete(0.0,END)
            self.dataGet.insert(INSERT,str(position()))
            self.dataGet.update()
    def start_getdata(self):
        '''另一线程实现开始、暂停、恢复获取实时点位'''
        if(self.getDataThread):
            if(self.__getDataFlag.isSet()):
                self.__getDataFlag.clear() # 暂停
            else:
                self.__getDataFlag.set() # 恢复

        else:
            self.getDataThread = threading.Thread(target=self.get_data)
            self.getDataThread.setDaemon(True)
            self.getDataThread.start()


if __name__ == '__main__':
    gui = Gui()
    gui.root.mainloop()