def CalculateTotalInStock(product):
    x = ((float(product["in_stock_kg"]) -
          (float(weights["third"]) * int(product["in_stock_third"]) +
           float(weights["double_third"]) * int(product["in_stock_double_third"]) + float(weights["box_dough"]) *
           int(product["in_stock_box_dough"]) + float(weights["ambat"]) * int(product["in_stock_ambat"]))) *
         float(product["kg"]) + float(product["box"]) * float(product["in_stock_box"]) + int(product["unit"]) * float(product["in_stock_unit"]))
    return round(x, 2)


def invalue(x, y):
    return round(x * y, 2)


weights = {
    "third": 0.66,
    "double_third": 1.015,
    "box_dough": 1.57,
    "ambat": 2.069
}
