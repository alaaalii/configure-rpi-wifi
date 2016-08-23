#!/usr/bin/env python

import os
import wx
import paramiko
import socket
import time


class Example(wx.Frame):

    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(420, 440))

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
        self.statusmessages = wx.StaticText(self.panel, label="Status Messages:")
        self.status = wx.StaticText(self.panel, label="")

        self.ip_tc = wx.TextCtrl(self.panel)
        self.username_tc = wx.TextCtrl(self.panel)
        self.password_tc = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        self.ssid_tc = wx.TextCtrl(self.panel)
        self.wifipassword_tc = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)

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

        self.sizer.Add(self.statusmessages, pos=(11, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)
        self.sizer.Add(self.status, pos=(12, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=self.border)

        self.sizer.AddGrowableCol(1)
        self.sizer.AddGrowableRow(4)

        self.panel.SetSizerAndFit(self.sizer)

        self.Bind(wx.EVT_BUTTON, self.OnQuitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_BUTTON, self.OnPush, id=wx.ID_SAVE)

    def OnQuitApp(self, event):

        self.Close()

    def OnPush(self, event):
        if not all([self.ip_tc.GetValue(), self.username_tc.GetValue(), self.password_tc.GetValue(), self.ssid_tc.GetValue(), self.wifipassword_tc.GetValue()]):
            self.status.SetLabel('[ERROR] Please enter a value for all fields.')
            return

        waitTime = 2

        self.push_btn.Disable()
        self.status.SetLabel('Connecting to RPi...')
        wx.Yield()
        #self.Refresh()
        #self.Update()

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()

        time.sleep(waitTime)

        try:
            client.connect(self.ip_tc.GetValue(), username=self.username_tc.GetValue(), password=self.password_tc.GetValue(), timeout=5)
        except socket.timeout:
            self.status.SetLabel('[ERROR] Could not communicate to RPi.')
            client.close()
            return
        except paramiko.ssh_exception.AuthenticationException:
            self.status.SetLabel('[ERROR] Authentication failed. Please make sure the username and password are correct.')
            client.close()
            return
        except Exception as e:
            self.status.SetLabel('[ERROR] Unknown error trying to connect to RPi')
            print str(e)
            client.close()
            return

        self.status.SetLabel('Connected...')
        wx.Yield()

        time.sleep(waitTime)

        stdin, stdout, stderr = client.exec_command('sudo ifup wlan0', timeout=2)

        time.sleep(waitTime)

        comm = '''sudo python -c "import wifi; print wifi.Cell.where('wlan0', lambda cell: cell.ssid.lower()=='{0}')[0]"'''.format(self.ssid_tc.GetValue().lower())
        stdin, stdout, stderr = client.exec_command(comm)
        retval = stdout.channel.recv_exit_status()
        out = stdout.readlines()
        err = stderr.readlines()
        if not(retval == 0 and any(self.ssid_tc.GetValue().lower() in item.lower() for item in out)):
            self.status.SetLabel('[ERROR] Could not find the wireless network')
            print "stdout from {0}:".format(comm)
            for line in out:
                print line.strip()
            client.close()
            return
        elif retval == 0:
            self.status.SetLabel('Found WiFi. Configuring...')
            wx.Yield()
        elif retval == 1:
            self.status.SetLabel('[ERROR] Unknown error trying to look for WiFi')
            print "stderr from {0}:".format(comm)
            for line in err:
                print line.strip()
            client.close()
            return

        time.sleep(waitTime)

        comm = '''sudo python -c "import wifi; scheme = wifi.Scheme.for_cell('wlan0', '{0}', wifi.Cell.where('wlan0', lambda cell: cell.ssid.lower()=='{1}')[0], '{2}'); scheme.save()"'''.format(self.ssid_tc.GetValue().lower().replace(' ', '_'), self.ssid_tc.GetValue().lower(), self.wifipassword_tc.GetValue())
        stdin, stdout, stderr = client.exec_command(comm)
        retval = stdout.channel.recv_exit_status()
        out = stdout.readlines()
        err = stderr.readlines()
        if retval == 0:
            self.status.SetLabel('Successfully configured RPi. Trying to connect to WiFi...')
            wx.Yield()
        elif retval == 1 and any('AssertionError: This scheme already exists' in item for item in err):
            self.status.SetLabel('Wireless network already saved on RPi. Connecting anyways...')
            wx.Yield()
        elif retval == 1:
            self.status.SetLabel('[ERROR] Unknown error trying to add WiFi configuration to RPi')
            print "stderr from {0}:".format(comm)
            for line in err:
                print line.strip()
            client.close()
            return

        time.sleep(waitTime)

        comm = '''sudo wifi autoconnect'''
        stdin, stdout, stderr = client.exec_command(comm, timeout=5)
        retval = stdout.channel.recv_exit_status()
        out = stdout.readlines()
        err = stderr.readlines()
        if retval == 0:
            self.status.SetLabel('Successfully connected to WiFi. Testing internet connection...')
            wx.Yield()
        elif retval == 1:
            self.status.SetLabel('[ERROR] Unknown error trying to connect to WiFi')
            print "stdout from {0}:".format(comm)
            for line in out:
                print line.strip()
                print
            print "stderr from {0}:".format(comm)
            for line in err:
                print line.strip()
            client.close()
            return

        time.sleep(waitTime)
        time.sleep(waitTime)

        comm = '''ping -w6 -c4 4.2.2.2'''
        stdin, stdout, stderr = client.exec_command(comm, timeout=8)
        retval = stdout.channel.recv_exit_status()
        out = stdout.readlines()
        err = stderr.readlines()
        if retval == 0:
            self.status.SetLabel('Successfully connected to internet. Done!')
            wx.Yield()
        elif retval == 1:
            self.status.SetLabel('[ERROR] Unknown error trying to check internet connection')
            print "stdout from {0}:".format(comm)
            for line in out:
                print line.strip()
                print
            print "stderr from {0}:".format(comm)
            for line in err:
                print line.strip()
            client.close()
            return

        client.close()
        return

if __name__ == '__main__':

    app = wx.App()
    frame = Example(None, title='RPi WiFi Configuration')
    frame.Centre()
    frame.Show()
    app.MainLoop()
