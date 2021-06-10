import wx
import uuid
import re
import hmac
import hashlib
from pubsub import pub

import Constants
from Database import db
import Queries


class RegisterDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, Constants.REGISTER_TITLE)
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
        # register
        self.register_btn = wx.Button(panel, -1, Constants.REGISTER_LABEL)
        self.register_btn.Bind(wx.EVT_BUTTON, self.OnRegister)
        vbox.Add(self.register_btn)
        panel.SetSizer(vbox)

    def OnRegister(self, event):
        try:
            db_cursor = db.cursor()
            db_cursor.execute(Queries.fetch_managers_email)
            managers_email = db_cursor.fetchall()
            if (self.isValidEmail(self.email_text.GetValue())):
                email = self.email_text.GetValue()
                # check for exist email
                for current_email in managers_email:
                    if current_email[0] == email:
                        raise Exception
                if (self.isValidPassword(self.password_text.GetValue())):
                    password = self.password_text.GetValue()
                    manager_id = str(uuid.uuid4())
                    encrypted_password = hmac.new(
                        bytes(manager_id[::-1], 'utf-8'), bytes(password,
                                                                'utf-8'), hashlib.sha1
                    )
                    query_values = (manager_id, email,
                                    encrypted_password.hexdigest())
                    db.cursor().execute(Queries.insert_to_managers, query_values)
                    db.commit()
                    wx.MessageBox(Constants.ADDED_MANAGER_SUCCESS_MESSAGE, Constants.SUCCESS,
                                  wx.OK | wx.ICON_INFORMATION)
                    self.Destroy()
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
