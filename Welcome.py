import wx
from pubsub import pub

import Constants
from LoginDialog import LoginDialog
from RegisterDialog import RegisterDialog


class Welcome(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, Constants.WELCOME_TITLE)
        pub.subscribe(self.OnLoginListener, Constants.ON_LOGIN_LISTENER)
        self.InitUI()

    def OnLoginListener(self, email):
        pub.sendMessage(Constants.ON_WELCOME_LISTENER, email=email)
        self.Destroy()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # login
        self.login_btn = wx.Button(panel, -1, Constants.LOGIN_LABEL)
        self.login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        vbox.Add(self.login_btn)
        # register
        self.register_btn = wx.Button(panel, -1, Constants.REGISTER_LABEL)
        self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegister)
        vbox.Add(self.register_btn)
        # set sizer
        panel.SetSizer(vbox)

    def OnLogin(self, event):
        login_dialog = LoginDialog(self).ShowModal()

    def OnRegister(self, event):
        register_dialog = RegisterDialog(self).ShowModal()
