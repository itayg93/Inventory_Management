# fetch manager by email
fetch_manager_by_email = '''
    SELECT * FROM Managers WHERE email = %s
'''

# fetch all managers email
fetch_managers_email = '''
    SELECT email FROM Managers
'''

# insert new manager to the managers table
insert_to_managers = '''
    INSERT INTO Managers (id, email, password) VALUES (%s, %s, %s)
'''

# fecth all the inventory
fetch_inventory = '''
    SELECT * FROM Inventory
'''

# insert new product to the inventory table
insert_to_inventory = '''
    INSERT INTO Inventory (id, supplier, product, size, price, kg, box, unit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
'''

# delete product from the inventory table by id
delete_from_inventory = '''
    DELETE FROM Inventory WHERE id = %s
'''

# update product in the inventory table by id
update_product = '''
    UPDATE Inventory SET price = %s, kg = %s, box = %s, unit = %s WHERE id = %s
'''
