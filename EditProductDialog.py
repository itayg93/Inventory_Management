import wx
from pubsub import pub

import Constants


class EditProductDialog(wx.Dialog):

    def __init__(self, parent, inventory):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           Constants.EDIT_PRODUCT_TITLE)
        self.inventory = inventory
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        selection_panel = wx.BoxSizer(wx.HORIZONTAL)
        select_product_label = wx.StaticText(
            panel, label=Constants.SELECT_PRODUCT_LABEL)
        selection_panel.Add(select_product_label, 1, wx.EXPAND |
                            wx.ALIGN_LEFT | wx.ALL, 5)
        # extract from inventory lists the products name
        products_name = []
        for product in self.inventory:
            products_name.append(product.get(
                Constants.PRODUCT_DICTIONARY_KEYS[2]))
        self.choice = wx.Choice(panel, choices=products_name)
        selection_panel.Add(
            self.choice, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)
        vbox.Add(selection_panel)
        # price
        price_hbox = wx.BoxSizer(wx.HORIZONTAL)
        price_label = wx.StaticText(panel, label=Constants.PRICE_LABEL)
        price_hbox.Add(price_label, 1, wx.EXPAND |
                       wx.ALIGN_LEFT | wx.ALL, 5)
        self.price = wx.TextCtrl(panel)
        self.price.Disable()
        price_hbox.Add(self.price)
        vbox.Add(price_hbox)
        # kg
        kg_hbox = wx.BoxSizer(wx.HORIZONTAL)
        kg_label = wx.StaticText(panel, label=Constants.KG_LABEL)
        kg_hbox.Add(kg_label, 1, wx.EXPAND |
                    wx.ALIGN_LEFT | wx.ALL, 5)
        self.kg = wx.TextCtrl(panel)
        self.kg.Disable()
        kg_hbox.Add(self.kg)
        vbox.Add(kg_hbox)
        # box
        box_hbox = wx.BoxSizer(wx.HORIZONTAL)
        box_label = wx.StaticText(panel, label=Constants.BOX_LABEL)
        box_hbox.Add(box_label, 1, wx.EXPAND |
                     wx.ALIGN_LEFT | wx.ALL, 5)
        self.box = wx.TextCtrl(panel)
        self.box.Disable()
        box_hbox.Add(self.box)
        vbox.Add(box_hbox)
        # unit
        unit_hbox = wx.BoxSizer(wx.HORIZONTAL)
        unit_label = wx.StaticText(panel, label=Constants.UNIT_LABEL)
        unit_hbox.Add(unit_label, 1, wx.EXPAND |
                      wx.ALIGN_LEFT | wx.ALL, 5)
        self.unit = wx.TextCtrl(panel)
        self.unit.Disable()
        unit_hbox.Add(self.unit)
        vbox.Add(unit_hbox)
        # edit
        edit_btn = wx.Button(panel, label=Constants.SAVE_LABEL)
        edit_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        vbox.Add(edit_btn, 1, wx.ALL, 5)
        panel.SetSizer(vbox)

    def OnChoice(self, event):
        self.index_of_product_to_edit = self.choice.GetSelection()
        product_to_edit = self.inventory[self.index_of_product_to_edit]
        #
        self.price.Enable()
        self.kg.Enable()
        self.box.Enable()
        self.unit.Enable()
        #
        self.price.SetValue(str(product_to_edit.get(
            Constants.PRODUCT_DICTIONARY_KEYS[4])))
        self.kg.SetValue(str(product_to_edit.get(
            Constants.PRODUCT_DICTIONARY_KEYS[5])))
        self.box.SetValue(str(product_to_edit.get(
            Constants.PRODUCT_DICTIONARY_KEYS[6])))
        self.unit.SetValue(str(product_to_edit.get(
            Constants.PRODUCT_DICTIONARY_KEYS[7])))

    def OnSave(self, event):
        editted_values = []
        editted_values.append(self.index_of_product_to_edit)
        editted_values.append(float(self.price.GetValue()))
        editted_values.append(float(self.kg.GetValue()))
        editted_values.append(float(self.box.GetValue()))
        editted_values.append(float(self.unit.GetValue()))
        pub.sendMessage(Constants.ON_EDIT_LISTENER,
                        editted_values=editted_values)
        self.Close()
