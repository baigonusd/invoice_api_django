import xlsxwriter
import pandas as pd


def save_file(items):
    df = pd.DataFrame()
    invoices = []
    products = []
    qtys = []
    prices = []
    amounts = []

    for item in items:
        invoices.append(item.invoice)
        products.append(item.product)
        qtys.append(item.qty)
        prices.append(item.price)
        amounts.append(item.amount)

    df["Invoices"] = invoices
    df["Products"] = products
    df["QTYs"] = qtys
    df["Prices"] = prices
    df["Amounts"] = amounts

    writer = pd.ExcelWriter(
        "./report.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="List1", index=False)

    writer.sheets["List1"].set_column("A:A", 30)
    writer.sheets["List1"].set_column("B:B", 30)
    writer.sheets["List1"].set_column("C:C", 30)
    writer.sheets["List1"].set_column("D:D", 30)
    writer.sheets["List1"].set_column("D:D", 30)

    writer.save()
