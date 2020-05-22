import json
import threading
from time import sleep
import requests

import tkinter as tk
from tkinter.filedialog import askdirectory
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/27.0.1453.94 '
                         'Safari/537.36 '}
api_comic_url = 'https://api.setu.cx/comic/'
api_album_url = 'https://api.setu.cx/album/'


class DownloadThread(threading.Thread):

    def __init__(self, linkUrl, savePath, picTitle, info):
        super(DownloadThread, self).__init__()
        self.linkUrl = linkUrl
        self.picTitle = picTitle
        self.savePath = savePath
        self.info = info
        self.path = ""

    def saveImage(self, content, path, number, context_name):
        if not os.path.isdir(str(path) + '\\' + str(context_name)):
            os.mkdir(str(path) + '\\' + str(context_name))
        with open(str(path) + '\\' + str(context_name) + '\\' + str(number) + '.jpg', 'wb') as f:
            try:
                f.write(content)
            except:
                self.info.insert(tk.END, "下载出错,不知道为什么...\n")

    def saveFromSite(self):
        self.info.insert(tk.END, "下载网址为" + self.linkUrl + "\n")
        self.info.insert(tk.END, "保存路径为" + self.savePath + "\n")
        child_url = self.linkUrl.split('?')[0].split('/')[-1]
        if child_url == '':
            self.info.insert(tk.END, "输入的网址格式不正确" + "...\n")
            return
        if 'comic' in self.linkUrl:
            url = api_comic_url + child_url
            try:
                requests.get(self.linkUrl)
                jsonContent = requests.get(url, headers=headers)
                jsonContent.encoding = 'utf-8'
                jsonDict = json.loads(jsonContent.text)
                print(jsonDict)
                number = 0
                for img_url in jsonDict.get('data').get('images'):
                    self.info.insert(tk.END, "正在下载第" + str(number) + "长图片从" + self.linkUrl + "\n")
                    img = requests.get(img_url, headers=headers)
                    number += 1
                    self.saveImage(img.content, self.savePath, number, child_url)
            finally:
                self.info.insert(tk.END, "可能网站访问错误")
        elif 'album' in self.linkUrl:
            url = api_album_url + child_url
            try:
                requests.get(self.linkUrl)
                jsonContent = requests.get(url, headers=headers)
                jsonContent.encoding = 'utf-8'
                jsonDict = json.loads(jsonContent.text)
                print(jsonDict)
                number = 0
                for img_url in jsonDict.get('data').get('pics_cdn_url'):
                    self.info.insert(tk.END, "正在下载第" + str(number) + "长图片从" + self.linkUrl + "\n")
                    img = requests.get(img_url, headers=headers)
                    number += 1
                    self.saveImage(img.content, self.savePath, number, child_url)
            finally:
                self.info.insert(tk.END, "可能网站访问错误")
        else:
            self.info.insert(tk.END, "抱歉,当前仅仅支持写真和动画" + "...\n")

    def run(self) -> None:
        self.saveFromSite()

class MainWindow:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SexTu")
        self.lab1 = tk.Label(self.window, text="保存路径:")
        self.save_input = tk.Entry(self.window, width=60)
        self.info = tk.Text(self.window, width=100, height=20)
        self.lab2 = tk.Label(self.window, text="URL(结尾不带/):")
        self.url_input = tk.Entry(self.window, width=60)
        self.t_button = tk.Button(self.window, text='选择路径', relief=tk.RAISED, width=8, height=1,
                                  command=self.select_path)
        self.t_button1 = tk.Button(self.window, text='下载', relief=tk.RAISED, width=8, height=1,
                                   command=self.hanleDownload)
        self.c_button2 = tk.Button(self.window, text='清空输出', relief=tk.RAISED, width=8, height=1,
                                   command=self.clear_input)

        self.lab1.grid(row=0, column=0)
        self.save_input.grid(row=0, column=1)
        self.t_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

        self.lab2.grid(row=1, column=0)
        self.url_input.grid(row=1, column=1)
        self.t_button1.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.c_button2.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)
        self.info.grid(row=2, rowspan=3, column=0, columnspan=5, padx=5, pady=5)
        self.info.insert(tk.END, "网站采用了保护措施,需要先打开一个网页,然后再请求该网页数据\n")

    def hanleDownload(self):
        url = self.url_input.get()
        path = self.save_input.get()
        downloadth = DownloadThread(url, path, url.split('?')[0].split('/')[-1], self.info)
        downloadth.setDaemon(True)
        downloadth.start()

    def select_path(self):
        self.save_input.delete(0, "end")
        self.save_input.insert(0, askdirectory())
        self.info.insert(tk.END, "已经选择目录...\n")

    def clear_input(self):
        self.info.delete(1.0, tk.END)


if __name__ == '__main__':
    window = MainWindow()
    tk.mainloop()
