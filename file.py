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
        label_sound.place(x=740,y=630,width=40,height=40)