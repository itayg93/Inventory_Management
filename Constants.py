# titles
WELCOME_TITLE = "Welcome"
LOGIN_TITLE = "Login"
REGISTER_TITLE = "Register"
INVENTORY_MANAGEMENT_TITLE = "Inventory Management"
ADD_PRODUCT_TITLE = "Add Product"
EDIT_PRODUCT_TITLE = "Edit Product"
DELETE_PRODUCT_TITLE = "Delete Product"

# dialogs listeners
ON_WELCOME_LISTENER = "OnWelcomeListener"
ON_LOGIN_LISTENER = "OnLoginListener"
ON_REGISTER_LISTENER = "OnRegisterListener"
ON_ADD_LISTENER = "OnAddListener"
ON_EDIT_LISTENER = "OnEditListener"
ON_DELETE_LISTENER = "OnDeleteListener"

# success messages
SUCCESS = "Success"
ADDED_MANAGER_SUCCESS_MESSAGE = "Manager successfully added!"
ADDED_SUCCESS_MESSAGE = "Product successfully added!"
UPDATE_SUCCESS_MESSAGE = "Product successfully updated!"
DELETE_SUCCESS_MESSAGE = "Product successfully deleted!"

# error messages
ERROR = "Error"
ERROR_MESSAGE = "Something went wrong!"
INVALID_EMAIL_ERROR_MESSAGE = "Enter valid email!"
INVALID_PASSWORD_ERROR_MESSAGE = "Enter valid password!"
WRONG_CREDENTIALS_ERROR_MESSAGE = "Wrong credentials!"

# labels
LOGIN_LABEL = "Login"
REGISTER_LABEL = "Register"
EMAIL_LABEL = "Email"
PASSWORD_LABEL = "Password"
ADD_LABEL = "Add"
EDIT_LABEL = "Edit"
DELETE_LABEL = "Delete"
SUPPLIER_LABEL = "Supplier"
PRODUCT_LABEL = "Product"
SIZE_LABEL = "Size"
KG_LABEL = "Kg"
UNIT_LABEL = "Unit"
BOX_LABEL = "Box"
LITER_LABEL = "Liter"
TIN_LABEL = "Tin"
PRICE_LABEL = "Price"
SAVE_LABEL = "Save"
SELECT_PRODUCT_LABEL = "Select Product"
CALCULATE_LABEL = "Calculate"
BRANCH_LABEL = "Branch"
MONTH_LABEL = "Month"
YEAR_LABEL = "Year"

#
BRANCHES = ["Allenby", "HaArba'a", "Rothschild", "Herzliya"]

#
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

#
PRODUCT_SIZES_OPTIONS = [KG_LABEL, UNIT_LABEL,
                         BOX_LABEL, LITER_LABEL, TIN_LABEL]

#
GRID_COLUMNS_LABELS = [SUPPLIER_LABEL, PRODUCT_LABEL, SIZE_LABEL, PRICE_LABEL, KG_LABEL, BOX_LABEL, UNIT_LABEL, "In-Stock Kg",
                       "In-Stock Box", "In-Stock Unit", "In-Stock Third", "In-Stock Double Third",
                       "In-Stock Box Dough", "In-Stock Bath", "Total In-Stock", "Inventory Value"]

#
PRODUCT_DICTIONARY_KEYS = ["product_id", "supplier", "product",
                           "size", "price", "kg", "box", "unit",
                           "in_stock_kg", "in_stock_box", "in_stock_unit",
                           "in_stock_third", "in_stock_double_third",
                           "in_stock_box_dough", "in_stock_ambat",
                           "total_in_stock", "inventory_value"]
