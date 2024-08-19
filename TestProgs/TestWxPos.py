#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TestWxPos.py
Created on Thu Aug 15 14:27:58 2024

From: https://wiki.wxpython.org/wxPython%20by%20Example

@author: slehar
"""

import wx


app = wx.App(redirect=True)
# top = wx.Frame(None, 
#                title="Hello World", 
#                size=(300,200),
#                pos=wx.Point(10,50)) 
               
top = wx.Frame(None, 
               title="Hello World", 
               size=(300,200)) 
               
wx.FRAME_FLOAT_ON_PARENT=True
# wx.STAY_ON_TOP=True
               
# wx.SYSTEM_MENU=True

top.SetPosition(wx.Point(50,300))

top.Show()

app.MainLoop()

