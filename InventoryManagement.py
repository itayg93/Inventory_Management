import wx
import wx.grid as gridlib
from pubsub import pub

import Constants
from Database import db
import Queries
from Welcome import Welcome
from AddProductDialog import AddProductDialog
from EditProductDialog import EditProductDialog
from DeleteProductDialog import DeleteProductDialog
import Calculations


class InventoryManagement(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          Constants.INVENTORY_MANAGEMENT_TITLE)
        pub.subscribe(self.OnWelcomeListener, Constants.ON_WELCOME_LISTENER)
        pub.subscribe(self.OnAddListener, Constants.ON_ADD_LISTENER)
        pub.subscribe(self.OnEditListener, Constants.ON_EDIT_LISTENER)
        pub.subscribe(self.OnDeleteListener, Constants.ON_DELETE_LISTENER)
        welcome = Welcome().Show()

    def OnWelcomeListener(self, email):
        self.InitUI(email)

    def OnAdd(self, event):
        add_product_dialog = AddProductDialog(self).ShowModal()

    def OnAddListener(self, new_product):
        # add new product to the self.inventory
        self.inventory.append(self.ProductAsDictionary(new_product))
        # insert the new product to the grid
        current_row = len(self.inventory)-1
        for index, data in enumerate(new_product[1:]):
            self.InsertIntoGrid(current_row, index, data)
        # add new product into inventory db
        try:
            db.cursor().execute(Queries.insert_to_inventory, new_product)
            db.commit()
            wx.MessageBox(Constants.ADDED_SUCCESS_MESSAGE, Constants.SUCCESS,
                          wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(Constants.ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            print(str(e))

    def OnEdit(self, event):
        edit_product_dialog = EditProductDialog(
            self, self.inventory).ShowModal()

    def OnEditListener(self, editted_values):
        index_to_edit = editted_values[0]
        # update self.inventory
        product_to_update = self.inventory[index_to_edit]
        # price, kg, box, unit
        product_to_update.update({Constants.PRODUCT_DICTIONARY_KEYS[4]: editted_values[1],
                                  Constants.PRODUCT_DICTIONARY_KEYS[5]: editted_values[2],
                                  Constants.PRODUCT_DICTIONARY_KEYS[6]: editted_values[3],
                                  Constants.PRODUCT_DICTIONARY_KEYS[7]: editted_values[4]})
        # update grid
        for column in range(4, 8):
            # column-1 -> because the table dont have id column
            self.InsertIntoGrid(index_to_edit, (column-1), str(
                product_to_update.get(Constants.PRODUCT_DICTIONARY_KEYS[column])))
        # update inventory table
        try:
            query_values = (editted_values[1], editted_values[2], editted_values[3],
                            editted_values[4], product_to_update.get(Constants.PRODUCT_DICTIONARY_KEYS[0]))
            db.cursor().execute(Queries.update_product, query_values)
            db.commit()
            wx.MessageBox(Constants.UPDATE_SUCCESS_MESSAGE, Constants.SUCCESS,
                          wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(Constants.ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            print(str(e))

    def OnDelete(self, event):
        delete_product_dialog = DeleteProductDialog(
            self, self.inventory).ShowModal()

    def OnDeleteListener(self, index_of_product_to_delete):
        # save the product id for finding later in the db
        product_id_to_delete = self.inventory[index_of_product_to_delete].get(
            Constants.PRODUCT_DICTIONARY_KEYS[0])
        # remove the product from the grid
        self.grid.DeleteRows(pos=index_of_product_to_delete,
                             numRows=1, updateLabels=True)
        # remove the product from self.inventory
        self.inventory.pop(index_of_product_to_delete)
        # remove the product from the inventory db
        try:
            query_values = (product_id_to_delete, )
            db.cursor().execute(Queries.delete_from_inventory, query_values)
            db.commit()
            wx.MessageBox(Constants.DELETE_SUCCESS_MESSAGE, Constants.SUCCESS,
                          wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(Constants.ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            print(str(e))

    def InitUI(self, email):
        self.Show()
        panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # email
        email_label = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        email_label.SetLabel(email)
        vbox.Add(email_label)
        # buttons
        buttons_hbox = wx.BoxSizer(wx.HORIZONTAL)
        # add
        add_btn = wx.Button(panel, label=Constants.ADD_LABEL)
        add_btn.Bind(wx.EVT_BUTTON, self.OnAdd)
        buttons_hbox.Add(add_btn)
        # edit
        edit_btn = wx.Button(panel, label=Constants.EDIT_LABEL)
        edit_btn.Bind(wx.EVT_BUTTON, self.OnEdit)
        buttons_hbox.Add(edit_btn)
        # delete
        delete_btn = wx.Button(panel, label=Constants.DELETE_LABEL)
        delete_btn.Bind(wx.EVT_BUTTON, self.OnDelete)
        buttons_hbox.Add(delete_btn)
        # calculate
        calculate_btn = wx.Button(panel, label=Constants.CALCULATE_LABEL)
        calculate_btn.Bind(wx.EVT_BUTTON, self.OnCalculate)
        buttons_hbox.Add(calculate_btn)
        # add buttons panel
        vbox.Add(buttons_hbox)
        # branch and date
        branch_and_date_hbox = wx.BoxSizer(wx.HORIZONTAL)
        # branch
        branch_label = wx.StaticText(panel, label=Constants.BRANCH_LABEL)
        branch_and_date_hbox.Add(branch_label)
        self.branch = wx.ComboBox(panel, choices=Constants.BRANCHES)
        branch_and_date_hbox.Add(self.branch)
        # month
        month_label = wx.StaticText(panel, label=Constants.MONTH_LABEL)
        branch_and_date_hbox.Add(month_label)
        self.month = wx.ComboBox(panel, choices=Constants.MONTHS)
        branch_and_date_hbox.Add(self.month)
        # year
        year_label = wx.StaticText(panel, label=Constants.YEAR_LABEL)
        branch_and_date_hbox.Add(year_label)
        self.year = wx.TextCtrl(panel)
        branch_and_date_hbox.Add(self.year)
        vbox.Add(branch_and_date_hbox)
        # grid
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(25, 16)
        vbox.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        # set vbox to panel
        panel.SetSizer(vbox)
        self.SetGridLabels()
        self.FetchInventory()
        # loop inside inventory array
        for row, product in enumerate(self.inventory):
            column = 0
            # loop inside the product dictionary
            for key in product:
                if key == Constants.PRODUCT_DICTIONARY_KEYS[0]:
                    continue
                self.InsertIntoGrid(row, column, product[key])
                column += 1

    def OnCalculate(self, event):
        for row, product in enumerate(self.inventory):
            # save user input in each product dictionary
            for column in range(7, 14):
                product[Constants.PRODUCT_DICTIONARY_KEYS[column+1]
                        ] = self.grid.GetCellValue(row, column)
            # calculate total in stock value
            product[Constants.PRODUCT_DICTIONARY_KEYS[15]] = Calculations.CalculateTotalInStock(
                product)
            # calculate inventory value
            product[Constants.PRODUCT_DICTIONARY_KEYS[16]] = product.get(
                Constants.PRODUCT_DICTIONARY_KEYS[15]) * float(product.get(Constants.PRODUCT_DICTIONARY_KEYS[4]))
            # show total in stock value in the grid
            self.grid.SetCellValue(row, 14, str(
                product.get(Constants.PRODUCT_DICTIONARY_KEYS[15])))
            # show inventory value in the grid
            self.grid.SetCellValue(row, 15, str(
                product.get(Constants.PRODUCT_DICTIONARY_KEYS[16])))

    def SetGridLabels(self):
        for index, label in enumerate(Constants.GRID_COLUMNS_LABELS):
            self.grid.SetColLabelValue(index, label)
        self.grid.AutoSizeColumns()

    def FetchInventory(self):
        self.inventory = []
        try:
            db_cursor = db.cursor()
            db_cursor.execute(Queries.fetch_inventory)
            inventory = db_cursor.fetchall()
            for product in inventory:
                self.inventory.append(self.ProductAsDictionary(product))
        except Exception as e:
            wx.MessageBox(Constants.ERROR_MESSAGE,
                          Constants.ERROR, wx.OK | wx.ICON_ERROR)
            print(str(e))

    def ProductAsDictionary(self, product):
        product_dictionary = {
            Constants.PRODUCT_DICTIONARY_KEYS[0]: product[0], Constants.PRODUCT_DICTIONARY_KEYS[1]: product[1],
            Constants.PRODUCT_DICTIONARY_KEYS[2]: product[2], Constants.PRODUCT_DICTIONARY_KEYS[3]: product[3],
            Constants.PRODUCT_DICTIONARY_KEYS[4]: product[4], Constants.PRODUCT_DICTIONARY_KEYS[5]: product[5],
            Constants.PRODUCT_DICTIONARY_KEYS[6]: product[6], Constants.PRODUCT_DICTIONARY_KEYS[7]: product[7],
            Constants.PRODUCT_DICTIONARY_KEYS[8]: "", Constants.PRODUCT_DICTIONARY_KEYS[9]: "", Constants.PRODUCT_DICTIONARY_KEYS[10]: "",
            Constants.PRODUCT_DICTIONARY_KEYS[11]: "", Constants.PRODUCT_DICTIONARY_KEYS[12]: "",
            Constants.PRODUCT_DICTIONARY_KEYS[13]: "", Constants.PRODUCT_DICTIONARY_KEYS[14]: "",
            Constants.PRODUCT_DICTIONARY_KEYS[15]: "", Constants.PRODUCT_DICTIONARY_KEYS[16]: ""
        }
        return product_dictionary

    def InsertIntoGrid(self, row, column, data):
        self.grid.SetCellValue(row, column, str(data))
        if column <= 6 or column > 13:
            self.grid.SetReadOnly(row, column)


def main():
    app = wx.App(False)
    inventory_management = InventoryManagement()
    app.MainLoop()


if __name__ == "__main__":
    main()
