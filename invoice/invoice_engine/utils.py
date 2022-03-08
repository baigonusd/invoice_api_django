import xlsxwriter
import pandas as pd
import openpyxl


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
    users = []
    products = []
    qtys = []
    prices = []
    amounts = []
    users_value = []
    for i in range(0, len(items)):
        users_value.append(list(items[i]))

        for data in items[i][users_value[i][0]]:
            users.append(users_value[i][0])
            products.append(data['product__title'])
            qtys.append(data['total_qty'])
            prices.append(data['price'])
            amounts.append(data['total_amount'])

    df = pd.DataFrame({'Users': users, 'Product': products, 'QTY': qtys,
                       'Price': prices, 'Amount': amounts})
    writer = pd.ExcelWriter(
        "./report_of_users.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="List1", index=False)

    writer.sheets["List1"].set_column("A:A", 30)
    writer.sheets["List1"].set_column("B:B", 30)
    writer.sheets["List1"].set_column("C:C", 30)
    writer.sheets["List1"].set_column("D:D", 30)
    writer.sheets["List1"].set_column("D:D", 30)

    writer.save()


def save_save(items):

    book = openpyxl.Workbook()

    sheet = book.active

    sheet['A1'] = 'User'
    sheet['B1'] = 'Product'
    sheet['C1'] = 'QTY'
    sheet['D1'] = 'Price'
    sheet['E1'] = 'Amount'

    row = 2
    users_value = []
    count = 0
    # for data in items
    for i in range(0, len(items)):
        users_value.append(list(items[i]))
        print('------------------')
        print(users_value[i][0])
        for data in items[i][users_value[i][0]]:

            if count == i:
                sheet[row][0].value = users_value[i][0]
                count += 1
            else:
                sheet[row][0].value = ' '
            sheet[row][1].value = data['product__title']
            sheet[row][2].value = data['total_qty']
            sheet[row][3].value = data['price']
            sheet[row][4].value = data['total_amount']
            row += 1

    book.save('save_book.xlsx')
