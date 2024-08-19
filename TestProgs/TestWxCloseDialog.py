#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TestWx.py
Created on Thu Aug 15 14:27:58 2024

From: https://wiki.wxpython.org/wxPython%20by%20Example

@author: slehar
"""

import wx

def OnClose(event):
    dlg = wx.MessageDialog(top, 
        "Do you really want to close this application?",
        "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    if result == wx.ID_OK:
        top.Destroy()




app = wx.App(redirect=True)
top = wx.Frame(None, title="Hello World", size=(300,200)) 
               
wx.FRAME_FLOAT_ON_PARENT=True
# wx.STAY_ON_TOP=True
               
top.Bind(wx.EVT_CLOSE, OnClose)

top.Show()

app.MainLoop()

