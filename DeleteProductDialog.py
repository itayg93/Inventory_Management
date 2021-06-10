import wx
from pubsub import pub

import Constants


class DeleteProductDialog(wx.Dialog):

    def __init__(self, parent, inventory):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           Constants.DELETE_PRODUCT_TITLE)
        self.inventory = inventory
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        select_product_label = wx.StaticText(
            panel, label=Constants.SELECT_PRODUCT_LABEL)
        hbox.Add(select_product_label, 1, wx.EXPAND |
                 wx.ALIGN_LEFT | wx.ALL, 5)
        # extract from inventory lists the products name
        products_name = []
        for product in self.inventory:
            products_name.append(product.get(
                Constants.PRODUCT_DICTIONARY_KEYS[2]))
        self.choice = wx.Choice(panel, choices=products_name)
        hbox.Add(self.choice, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)
        delete_btn = wx.Button(panel, label=Constants.DELETE_LABEL)
        delete_btn.Bind(wx.EVT_BUTTON, self.OnDelete)
        hbox.Add(delete_btn, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        panel.SetSizer(hbox)

    def OnChoice(self, event):
        self.index_of_product_to_delete = self.choice.GetSelection()

    def OnDelete(self, event):
        pub.sendMessage(
            Constants.ON_DELETE_LISTENER, index_of_product_to_delete=self.index_of_product_to_delete)
        self.Close()
