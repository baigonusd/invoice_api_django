import xlsxwriter
import pandas as pd


def save_file(items):
    df = pd.DataFrame()
    users = []
    titles = []
    contracts = []
    products = []
    prices = []
    numbers = []
    sums = []

    for invoice in items:
        users.append(invoice.user)
        titles.append(invoice.title)
        contracts.append(invoice.contract)
        products.append(invoice.product)
        prices.append(invoice.price)
        numbers.append(invoice.number)
        sums.append(invoice.sum)

    df["Users"] = users
    df["Titles"] = titles
    df["Contracts"] = contracts
    df["Products"] = products
    df["Prices"] = prices
    df["Numbers"] = numbers
    df["Sum"] = sums

    writer = pd.ExcelWriter(
        "./invoice_engine/report.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="List1", index=False)

    writer.sheets["List1"].set_column("A:A", 30)
    writer.sheets["List1"].set_column("B:B", 30)
    writer.sheets["List1"].set_column("C:C", 30)
    writer.sheets["List1"].set_column("D:D", 30)
    writer.sheets["List1"].set_column("E:E", 30)
    writer.sheets["List1"].set_column("F:F", 30)

    writer.save()
