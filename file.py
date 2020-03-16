# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:38:45 2019

@author: DELL
"""

import requests
import pygame
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import ttk
class music():
    
    def __init__(self, master):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        self.root=master
        self.root.geometry('1000x700')
        self.pause=True
        self.flag=0
        self.varid=tk.StringVar()
        self.varplay=tk.StringVar()

        global img_search
        global img_background
        global img_play
        global img_pause
        global img_next
        global img_last
        global img_sound

        global img_download
        global img_music

        im_search=Image.open('search.png')
        im_bk = Image.open("background.png")
        im_play=Image.open('play.png')
        im_pause=Image.open('pause.png')
        im_next=Image.open('next.png')
        im_last=Image.open('last.png')
        im_sound=Image.open('sound.png')
        im_download=Image.open('download.png')
        im_music=Image.open('music.png')

        img_search=ImageTk.PhotoImage(im_search)
        img_background = ImageTk.PhotoImage(im_bk)
        img_play = ImageTk.PhotoImage(im_play)
        img_pause =ImageTk.PhotoImage(im_pause)
        img_next = ImageTk.PhotoImage(im_next)
        img_last = ImageTk.PhotoImage(im_last)
        img_sound=ImageTk.PhotoImage(im_sound)
        img_download=ImageTk.PhotoImage(im_download)
        img_music=ImageTk.PhotoImage(im_music)

        imLabel = tk.Label(self.root, image=img_background)
        imLabel.place(x=0,y=0,width=1000,height=700)
        label_music=tk.Label(self.root,image=img_music)
        label_music.place(x=10, y=610, width=80, height=80)

        self.ybar = ttk.Scrollbar(self.root)
        self.ybar.place(x=970,y=100,width=20,height=500)
        self.tree=ttk.Treeview(self.root, show="headings", columns=('col1','col2','col3','col4','col5'),yscrollcommand=self.ybar.set)
        self.tree.place(x=10, y=100, width=960, height=500)
        self.ybar.configure(command=self.tree.yview)
        #tree.yview是tree的回调函数，ybar.set是ybar的回调函数，两者互相调用给对方的相应命令，实现滚动条

        self.tree.column('col1', width=50, anchor='center')
        self.tree.column('col2', width=310, anchor='center')
        self.tree.column('col3', width=100, anchor='center')
        self.tree.column('col4', width=100, anchor='center')
        self.tree.column('col5', width=400, anchor='center')

        self.tree.heading('col1', text='序号')
        self.tree.heading('col2', text='歌名')
        self.tree.heading('col3', text='时长')
        self.tree.heading('col4', text='歌手')
        self.tree.heading('col5', text='专辑')

        self.entryid = tk.Entry(self.root, textvariable=self.varid)
        self.entryid.place(x=790, y=25, width=200, height=50)


        button_search=tk.Button(self.root, image=img_search, command=self.show)
        button_search.place(x=730, y=25, width=50, height=50)


        button_last = tk.Button(self.root, image=img_last, command=self.btn_lastplay)
        button_last.place(x=100, y=615, width=70, height=70)

        self.button_play=tk.Button(self.root, image=img_play, command=self.btnplay)
        self.button_play.place(x=180, y=610, width=80, height=80)

        button_next=tk.Button(self.root,image=img_next,command=self.btnnextplay)
        button_next.place(x=270,y=615,width=70,height=70)

        button_download=tk.Button(self.root,image=img_download,command=self.download)
        button_download.place(x=350,y=615,width=70,height=70)

        self.soundscale=tk.Scale(self.root,from_=0,to=100,orient='horizontal',resolution=1,command=self.sound)
        #Scale的command回调函数自带相应的数值，将该值通过比例变换后赋值给音量设置函数即可完成音量调节
        self.soundscale.place(x=790,y=630,width=200,height=40)
        self.soundscale.set(20)
        label_sound=tk.Label(self.root,image=img_sound)
        label_sound.place(x=740, y=630, width=40, height=40)
    def sound(self,x):
        sound_=int(x)/100
        pygame.mixer.music.set_volume(sound_)


    def changetime(self,x):
        m=(x/1000)//60
        s=str(int((x/1000)%60))
        if len(s)==1:
            s='0'+s
        return ('%d:%s' % (m, s))
    def show(self):
        #通过歌单api链接得到返回值并解码
        searchid=self.entryid.get()
        url='http://music.163.com/api/playlist/detail?id=%s'%searchid
        r = requests.get(url)
        self.songlist = r.json()
        #形成歌单列表
        for i in range(len(self.songlist['result']['tracks'])):
            song = self.songlist['result']['tracks'][i]['name']
            id =self.songlist['result']['tracks'][i]['id']
            duration = self.changetime(int(self.songlist['result']['tracks'][i]['duration']))
            artist = self.songlist['result']['tracks'][i]['artists'][0]['name']
            album = self.songlist['result']['tracks'][i]['album']['name']
            self.tree.insert('',i, values = ('%s'%i, '%s'%song , '%s'%duration, '%s'%artist,'%s'%album))
        #歌单封面图片
        url_listpic=self.songlist['result']['coverImgUrl']
        r_listpic = requests.get(url_listpic)
        with open('%s.jpg' % searchid, 'wb') as p:#将图片下载到本地
            p.write(r_listpic.content)
        im_list = Image.open('%s.jpg' % searchid)
        global img_list
        img_list = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_list))
        labelimg_list = tk.Label(self.root, image=img_list)
        labelimg_list.place(x=10, y=10, width=80, height=80)
        #歌单文字信息
        list_name=self.songlist['result']['name']
        list_description=self.songlist['result']['description']
        list_playcount=self.songlist['result']['playCount']
        label_name=tk.Label(self.root,text=list_name,font=(r'c:\windows\fonts\simsun.ttc',20),anchor='w')
        label_name.place(x=100,y=10,width=500,height=30)
        label_description=tk.Label(self.root,text=list_description,font=(r'c:\windows\fonts\simsun.ttc',8),anchor='w',justify='left')
        label_description.place(x=100,y=45,width=600,height=25)
        label_count=tk.Label(self.root,text='播放次数:'+str(list_playcount),font=(r'c:\windows\fonts\simsun.ttc',10),anchor='w')
        label_count.place(x=100,y=75,width=200,height=15)
    def Resize(self,w_box, h_box, pil_image):  # 参数是：要适应的窗口宽、高、Image.open后的图片
        w, h = pil_image.size  # 获取图像的原始大小
        f1 = 1.0 * w_box / w#获取高、宽的现有与标准的比例
        f2 = 1.0 * h_box / h
        factor = min([f1, f2])#取其中较小的作为需要缩放的比例
        width = int(w * factor)
        height = int(h * factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def download(self):#下载键
        for item in self.tree.selection():#获取选中项目
            item_text=self.tree.item(item,'value')
        id = self.songlist['result']['tracks'][int(item_text[0])]['id']
        url_song = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % id
        r_song = requests.get(url_song)
        with open('%s.mp3' % id, 'wb') as s:#下载相应歌曲
            s.write(r_song.content)

        # 获取选中歌曲封面
        pic = self.songlist['result']['tracks'][int(item_text[0])]['album']['picUrl']
        url_pic = pic
        r_pic = requests.get(url_pic)
        with open('%s.jpg' % id, 'wb') as p:
            p.write(r_pic.content)
        im_song = Image.open('%s.jpg' % id)
        global img_song
        img_song = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_song))
        labelimg_song = tk.Label(self.root, image=img_song)
        labelimg_song.place(x=10, y=610, width=80, height=80)

    def btnplay(self):
        #获取选中项目
        for item in self.tree.selection():
            item_text=self.tree.item(item,'value')

        if self.pause==True:#暂停状态
            if self.flag==0:#是第一次播放，则需下载歌曲
                #歌曲播放
                id = self.songlist['result']['tracks'][int(item_text[0])]['id']
                url_song='http://music.163.com/song/media/outer/url?id=%s.mp3'%id
                r_song = requests.get(url_song)
                with open('%s.mp3'%id,'wb') as s:#下载到本地
                    s.write(r_song.content)
                #播放歌曲
                pygame.mixer.music.load('F:\北航\学习\大计基\大作业\%s.mp3'%id)
                pygame.mixer.music.play()
                self.button_play['image'] = img_pause#切换按钮显示的图片
                self.pause = False
                self.flag = 1
                #歌曲封面
                pic = self.songlist['result']['tracks'][int(item_text[0])]['album']['picUrl']
                url_pic = pic
                r_pic = requests.get(url_pic)
                with open('%s.jpg'%id,'wb') as p:#将图片下载到本地
                    p.write(r_pic.content)
                im_song1 = Image.open('%s.jpg'%id)
                global img_song1
                img_song1=ImageTk.PhotoImage(self.Resize(80.0,80.0,im_song1))
                labelimg_song1=tk.Label(self.root,image=img_song1)
                labelimg_song1.place(x=10,y=610,width=80,height=80)


            else:#如果不是第一次播放，则直接开始播放
                pygame.mixer.music.unpause()
                self.button_play['image']=img_pause#图片切换
                self.pause=False
        else:#若为播放状态
            pygame.mixer.music.pause()
            self.pause=True
            self.button_play['image'] = img_play
    def btnnextplay(self):
        for item in self.tree.selection():
            item_text=self.tree.item(item,'value')
        nextplay_id=self.songlist['result']['tracks'][int(item_text[0])+1]['id']
        global img_nextsong
        if self.pause==True:
            self.button_play['image']=img_pause
            self.pause = False
            url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % nextplay_id
            r = requests.get(url)
            with open('%s.mp3' % nextplay_id, 'wb') as s:
                s.write(r.content)
            pygame.mixer.music.load('F:\北航\学习\大计基\大作业\%s.mp3' % nextplay_id)
            pygame.mixer.music.play()

            pic = self.songlist['result']['tracks'][int(item_text[0]) + 1]['album']['picUrl']
            url_pic = pic
            r_pic = requests.get(url_pic)
            with open('%s.jpg' % nextplay_id, 'wb') as p:
                p.write(r_pic.content)
            im_nextsong = Image.open('%s.jpg' % nextplay_id)

            img_nextsong = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_nextsong))
            labelimg_song = tk.Label(self.root, image=img_nextsong)
            labelimg_song.place(x=10, y=610, width=80, height=80)
        else:
            self.button_play['image'] = img_pause
            url='http://music.163.com/song/media/outer/url?id=%s.mp3'%nextplay_id
            r=requests.get(url)
            with open('%s.mp3'%nextplay_id,'wb') as s:
                s.write(r.content)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('F:\北航\学习\大计基\大作业\%s.mp3'%nextplay_id)
            pygame.mixer.music.play()

            pic = self.songlist['result']['tracks'][int(item_text[0])+1]['album']['picUrl']
            url_pic=pic
            r_pic = requests.get(url_pic)
            with open('%s.jpg' % nextplay_id, 'wb') as p:
                p.write(r_pic.content)
            im_nextsong = Image.open('%s.jpg' % nextplay_id)
            img_nextsong = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_nextsong))
            labelimg_song = tk.Label(self.root, image=img_nextsong)
            labelimg_song.place(x=10, y=610, width=80, height=80)

    def btn_lastplay(self):
        for item in self.tree.selection():
            item_text=self.tree.item(item,'value')
        global img_lastsong

        if self.pause==True:
            self.button_play['image']=img_pause
            self.pause = False
            self.button_play['image'] = img_pause
            lastplay_id = self.songlist['result']['tracks'][int(item_text[0]) - 1]['id']
            url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' % lastplay_id
            r = requests.get(url)
            with open('%s.mp3' % lastplay_id, 'wb') as s:
                s.write(r.content)
            pygame.mixer.music.load('F:\北航\学习\大计基\大作业\%s.mp3' % lastplay_id)
            pygame.mixer.music.play()

            pic = self.songlist['result']['tracks'][int(item_text[0]) - 1]['album']['picUrl']
            url_pic = pic
            r_pic = requests.get(url_pic)
            with open('%s.jpg' % lastplay_id, 'wb') as p:
                p.write(r_pic.content)
            im_lastsong = Image.open('%s.jpg' % lastplay_id)

            img_lastsong = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_lastsong))
            labelimg_song = tk.Label(self.root, image=img_lastsong)
            labelimg_song.place(x=10, y=610, width=80, height=80)
        else:
            self.button_play['image']=img_pause
            lastplay_id=self.songlist['result']['tracks'][int(item_text[0])-1]['id']
            url='http://music.163.com/song/media/outer/url?id=%s.mp3'%lastplay_id
            r=requests.get(url)
            with open('%s.mp3'%lastplay_id,'wb') as s:
                s.write(r.content)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('F:\北航\学习\大计基\大作业\%s.mp3'%lastplay_id)
            pygame.mixer.music.play()

            pic = self.songlist['result']['tracks'][int(item_text[0])-1]['album']['picUrl']
            url_pic = pic
            r_pic = requests.get(url_pic)
            with open('%s.jpg' % lastplay_id, 'wb') as p:
                p.write(r_pic.content)
            im_lastsong = Image.open('%s.jpg' % lastplay_id)
            img_lastsong = ImageTk.PhotoImage(self.Resize(80.0, 80.0, im_lastsong))
            labelimg_song = tk.Label(self.root, image=img_lastsong)
            labelimg_song.place(x=10, y=610, width=80, height=80)



base=tk.Tk()
music(base)
base.mainloop()