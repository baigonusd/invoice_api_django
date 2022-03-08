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


def save_report(items):
    # df = pd.DataFrame()
    users = []
    products = []
    qtys = []
    prices = []
    amounts = []

    # for item in items.keys():
    #     users.append(item)
    #     for data in items[item]:
    #         products.append(data['product__title'])
    #         qtys.append(data['total_qty'])
    #         prices.append(data['price'])
    #         amounts.append(data['total_amount'])
    users_value = []
    count = 0
    for i in range(0, len(items)):
        users_value.append(list(items[i]))

        for data in items[i][users_value[i][0]]:
            users.append(users_value[i][0])
            products.append(data['product__title'])
            qtys.append(data['total_qty'])
            prices.append(data['price'])
            amounts.append(data['total_amount'])

    df = pd.DataFrame({'Users': users, 'Product': products, 'qty': qtys,
                       'price': prices, 'amount': amounts})
    # df["User"] = pd.Series(users)

    # df = pd.DataFrame({'Product': products, 'qty': qtys,
    #                    'price': prices, 'amount': amounts})
    # df["User"] = pd.Series(users)
    # a = items[i]
    # print(items.keys())
    # print(users)
    # print(products)
    # print(qtys)

    # df["Product"] = products
    # df["QTY"] = qtys
    # df["Price"] = prices
    # df["Amount"] = amounts

    writer = pd.ExcelWriter(
        "./report_of_users.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="List1", index=False)

    writer.sheets["List1"].set_column("A:A", 30)
    writer.sheets["List1"].set_column("B:B", 30)
    writer.sheets["List1"].set_column("C:C", 30)
    writer.sheets["List1"].set_column("D:D", 30)
    writer.sheets["List1"].set_column("D:D", 30)

    writer.save()
