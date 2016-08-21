#!/usr/bin/env python

import os
import wx


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(420, 340))

        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(4, 4)

        self.border = 5

        self.rpi = wx.StaticText(self.panel, label="RPi Settings")
        self.ip = wx.StaticText(self.panel, label="IP Address")
        self.username = wx.StaticText(self.panel, label="Username")
        self.password = wx.StaticText(self.panel, label="Password")
        self.wifi = wx.StaticText(self.panel, label="WiFi Settings")
        self.ssid = wx.StaticText(self.panel, label="SSID")
        self.wifipassword = wx.StaticText(self.panel, label="Password")

        self.ip_tc = wx.TextCtrl(self.panel)
        self.username_tc = wx.TextCtrl(self.panel)
        self.password_tc = wx.TextCtrl(self.panel)
        self.ssid_tc = wx.TextCtrl(self.panel)
        self.wifipassword_tc = wx.TextCtrl(self.panel)

        self.push_btn = wx.Button(self.panel, wx.ID_SAVE, label='Push', size=(70, 30))
        self.close_btn = wx.Button(self.panel, wx.ID_EXIT, label='Close', size=(70, 30))

        self.sizer.Add(self.rpi, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.ip, pos=(1, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.ip_tc, pos=(1, 1), span=(1, 5), flag=wx.EXPAND|wx.RIGHT, border=self.border)
        self.sizer.Add(self.username, pos=(2, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.username_tc, pos=(2, 1), span=(1, 5), flag=wx.EXPAND|wx.RIGHT, border=self.border)
        self.sizer.Add(self.password, pos=(3, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.password_tc, pos=(3, 1), span=(1, 5), flag=wx.EXPAND|wx.RIGHT, border=self.border)

        self.sizer.Add(self.wifi, pos=(5, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.ssid, pos=(6, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.ssid_tc, pos=(6, 1), span=(1, 5), flag=wx.EXPAND|wx.RIGHT, border=self.border)
        self.sizer.Add(self.wifipassword, pos=(7, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.wifipassword_tc, pos=(7, 1), span=(1, 5), flag=wx.EXPAND|wx.RIGHT, border=self.border)

        self.sizer.Add(self.push_btn, pos=(9, 0), flag=wx.EXPAND|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.close_btn, pos=(9, 4), flag=wx.EXPAND|wx.RIGHT|wx.BOTTOM, border=self.border)

        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(4)

        self.panel.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.OnPush, id=wx.ID_SAVE)

    def OnQuitApp(self, event):

        self.Close()

    def OnPush(self, event):
        print self.ip_tc.GetValue()

if __name__ == '__main__':

    app = wx.App()
    frame = Example(None, title='RPi WiFi Configuration')
    frame.Centre()
    frame.Show()
    app.MainLoop()
