import wx
import uuid
from pubsub import pub

import Constants


class AddProductDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           Constants.ADD_PRODUCT_TITLE, size=(350,350))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # supplier
        supplier_hbox = wx.BoxSizer(wx.HORIZONTAL)
        supplier_label = wx.StaticText(panel, label=Constants.SUPPLIER_LABEL)
        supplier_hbox.Add(supplier_label, 1, wx.EXPAND |
                          wx.ALIGN_LEFT | wx.ALL, 5)
        self.s_name = wx.TextCtrl(panel, size=(120, 30))
        supplier_hbox.Add(self.s_name, 1, wx.EXPAND |
                          wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(supplier_hbox)
        # product
        product_hbox = wx.BoxSizer(wx.HORIZONTAL)
        product_label = wx.StaticText(panel, label=Constants.PRODUCT_LABEL)
        product_hbox.Add(product_label, 1, wx.EXPAND |
                         wx.ALIGN_LEFT | wx.ALL, 5)
        self.p_name = wx.TextCtrl(panel, size=(120, 30))
        product_hbox.Add(self.p_name)
        vbox.Add(product_hbox)
        # size
        size_hbox = wx.BoxSizer(wx.HORIZONTAL)
        size_label = wx.StaticText(panel, label=Constants.SIZE_LABEL)
        size_hbox.Add(size_label, 1, wx.EXPAND |
                      wx.ALIGN_LEFT | wx.ALL, 5)
        self.combo = wx.ComboBox(
            panel, choices=Constants.PRODUCT_SIZES_OPTIONS, size=(90, 30))
        size_hbox.Add(self.combo)
        vbox.Add(size_hbox)
        # price
        price_hbox = wx.BoxSizer(wx.HORIZONTAL)
        price_label = wx.StaticText(panel, label=Constants.PRICE_LABEL)
        price_hbox.Add(price_label, 1, wx.EXPAND |
                       wx.ALIGN_LEFT | wx.ALL, 5)
        self.price = wx.TextCtrl(panel)
        price_hbox.Add(self.price)
        vbox.Add(price_hbox)
        # kg
        kg_hbox = wx.BoxSizer(wx.HORIZONTAL)
        kg_label = wx.StaticText(panel, label=Constants.KG_LABEL)
        kg_hbox.Add(kg_label, 1, wx.EXPAND |
                    wx.ALIGN_LEFT | wx.ALL, 5)
        self.kg = wx.TextCtrl(panel)
        kg_hbox.Add(self.kg)
        vbox.Add(kg_hbox)
        # box
        box_hbox = wx.BoxSizer(wx.HORIZONTAL)
        box_label = wx.StaticText(panel, label=Constants.BOX_LABEL)
        box_hbox.Add(box_label, 1, wx.EXPAND |
                     wx.ALIGN_LEFT | wx.ALL, 5)
        self.box = wx.TextCtrl(panel)
        box_hbox.Add(self.box)
        vbox.Add(box_hbox)
        # unit
        unit_hbox = wx.BoxSizer(wx.HORIZONTAL)
        unit_label = wx.StaticText(panel, label=Constants.UNIT_LABEL)
        unit_hbox.Add(unit_label, 1, wx.EXPAND |
                      wx.ALIGN_LEFT | wx.ALL, 5)
        self.unit = wx.TextCtrl(panel)
        unit_hbox.Add(self.unit)
        vbox.Add(unit_hbox)
        # add
        add_btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = wx.Button(panel, label=Constants.ADD_LABEL)
        add_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        add_btn_hbox.Add(add_btn, wx.EXPAND |
                         wx.ALIGN_LEFT | wx.ALL, 5)
        vbox.Add(add_btn_hbox)
        panel.SetSizer(vbox)

    def OnSave(self, event):
        new_product = []
        new_product.append(str(uuid.uuid4()))
        new_product.append(self.s_name.GetValue())
        new_product.append(self.p_name.GetValue())
        new_product.append(self.combo.GetValue())
        new_product.append(self.price.GetValue())
        new_product.append(self.kg.GetValue())
        new_product.append(self.box.GetValue())
        new_product.append(self.unit.GetValue())
        pub.sendMessage(Constants.ON_ADD_LISTENER, new_product=new_product)
        self.Close()
