import pandas as pd

# Load project datasets
inventory = pd.read_csv("data/inventory.csv")
sales = pd.read_csv("data/sales.csv")
suppliers = pd.read_csv("data/suppliers.csv")


# TOOL 1: Inventory Analysis
def inventory_lookup():
    return inventory


# TOOL 2: Sales Analysis
def sales_analysis(product_id):
    product_sales = sales[sales["product_id"] == product_id]

    if product_sales.empty:
        return None

    total_sales = product_sales["units_sold"].sum()
    average_monthly_sales = total_sales / len(product_sales)

    return average_monthly_sales


# TOOL 3: Stockout Risk Detection
def detect_stockout_risk():
    results = []

    for _, product in inventory.iterrows():

        stock = product["current_stock"]
        demand = product["daily_demand"]
        safety = product["safety_stock"]

        lead_time = suppliers[
            suppliers["product_id"] == product["product_id"]
        ]["delivery_days"].min()

        reorder_point = (demand * lead_time) + safety

        if stock < demand * lead_time:
            risk = "CRITICAL"
        elif stock < reorder_point:
            risk = "HIGH"
        else:
            risk = "LOW"

        results.append({
            "Product": product["product_name"],
            "Current Stock": stock,
            "Reorder Point": reorder_point,
            "Risk": risk
        })

    return pd.DataFrame(results)


# TOOL 4: Supplier Comparison
def supplier_comparison(product_id):

    result = suppliers[
        suppliers["product_id"] == product_id
    ].sort_values(by="cost_per_unit")

    return result


# TOOL 5: Purchase Quantity Recommendation
def reorder_calculation(product_id):

    product = inventory[
        inventory["product_id"] == product_id
    ]

    if product.empty:
        return None

    stock = product.iloc[0]["current_stock"]
    demand = product.iloc[0]["daily_demand"]
    safety = product.iloc[0]["safety_stock"]

    target_stock = (demand * 7) + safety
    purchase_quantity = max(0, target_stock - stock)

    return purchase_quantity


# TEST THE TOOLS
if __name__ == "__main__":

    print("\nSUPPLYCHAINIQ INVENTORY ANALYSIS")
    print(inventory_lookup())

    print("\nSTOCKOUT RISK ANALYSIS")
    print(detect_stockout_risk())

    print("\nSUPPLIER COMPARISON FOR LAPTOP")
    print(supplier_comparison("P001"))

    print("\nRECOMMENDED LAPTOP PURCHASE QUANTITY")
    print(reorder_calculation("P001"))