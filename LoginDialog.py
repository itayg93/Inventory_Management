import wx
import re
import hmac
import hashlib
from pubsub import pub

import Constants
from Database import db
import Queries


class WrongCredentials(Exception):
    pass


class LoginDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, Constants.LOGIN_TITLE)
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # email
        email_hbox = wx.BoxSizer(wx.HORIZONTAL)
        email_label = wx.StaticText(panel, -1, Constants.EMAIL_LABEL)
        self.email_text = wx.TextCtrl(panel, size=(175, 40))
        email_hbox.Add(email_label, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        email_hbox.Add(self.email_text, 1, wx.EXPAND |
                       wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(email_hbox)
        # password
        password_hbox = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(
            panel, -1, Constants.PASSWORD_LABEL)
        self.password_text = wx.TextCtrl(
            panel, size=(175, 40), style=wx.TE_PASSWORD)
        password_hbox.Add(password_label, 1, wx.EXPAND |
                          wx.ALIGN_LEFT | wx.ALL, 5)
        password_hbox.Add(self.password_text, 1, wx.EXPAND |
                          wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(password_hbox)
        # login
        self.login_btn = wx.Button(panel, -1, Constants.LOGIN_LABEL)
        self.login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        vbox.Add(self.login_btn)
        panel.SetSizer(vbox)

    def OnLogin(self, event):
        try:
            if (self.isValidEmail(self.email_text.GetValue())):
                email = self.email_text.GetValue()
                if (self.isValidPassword(self.password_text.GetValue())):
                    password = self.password_text.GetValue()
                    db_cursor = db.cursor()
                    query_values = (email, )
                    db_cursor.execute(
                        Queries.fetch_manager_by_email, query_values)
                    query_result = db_cursor.fetchone()
                    encrypted_password = hmac.new(
                        bytes(query_result[0][::-1], 'utf-8'), bytes(password,
                                                                     'utf-8'), hashlib.sha1
                    )
                    if query_result[2] != encrypted_password.hexdigest():
                        raise WrongCredentials
                    pub.sendMessage(
                        Constants.ON_LOGIN_LISTENER, email=email)
                    self.Destroy()
        except WrongCredentials:
            wx.MessageBox(Constants.WRONG_CREDENTIALS_ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(Constants.ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            print(str(e))

    def isValidEmail(self, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            wx.MessageBox(Constants.INVALID_EMAIL_ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            return False

    def isValidPassword(self, password):
        password_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,25}$"
        base = re.compile(password_regex)
        if re.search(base, password):
            return True
        else:
            wx.MessageBox(Constants.INVALID_PASSWORD_ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            return False
