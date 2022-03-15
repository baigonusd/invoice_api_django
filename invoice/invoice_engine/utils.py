import openpyxl
import datetime

from core.models import User
from invoice_engine.serializers import InvoiceItemSerializer
from invoice_engine.models import Invoice, InvoiceItem
from django.db.models import Sum


def create_xlsx(date_f, date_l):
    items = []

    for user in User.objects.all():
        a = user.invoices.filter(user=user, date__gte=date_f, date__lte=date_l).values(
            'item__product__title', 'item__product__price').annotate(total_qty=Sum('item__qty'), total_amount=Sum('item__amount'))
        items.append({user.email: a})

    if not items:
        raise Exception("NO DATA")

    # items = [{users[i].email: list(InvoiceItem.objects.values('product__title', 'product__price').filter(
    #     invoice__user__id=i+1, invoice__date__gte=f'2022-0{month}-01', invoice__date__lt=f'2022-0{month+1}-01').annotate(total_qty=Sum('qty')).annotate(total_amount=Sum('amount')))} for i in range(len(users))]

    book = openpyxl.Workbook()

    sheet = book.active

    sheet['A1'] = 'User'
    sheet['B1'] = 'Product'
    sheet['C1'] = 'QTY'
    sheet['D1'] = 'Price'
    sheet['E1'] = 'Amount'
    sheet['F1'] = 'Sum'

    row = 2
    # users_value = []
    count = 0
    sum = []

    for i in range(len(items)):
        sum_items = 0
        for data in items[i][list(items[i])[0]]:
            sum_items += data['total_amount']
        sum.append(sum_items)

    # for data in items
    for i in range(0, len(items)):
        # users_value.append(list(items[i]))

        for data in items[i][list(items[i])[0]]:

            if count == i:
                sheet[row][0].value = list(items[i])[0]
                sheet[row][5].value = sum[i]
                count += 1
            else:
                sheet[row][0].value = ' '
                sheet[row][5].value = ' '

            sheet[row][1].value = data['item__product__title']
            sheet[row][2].value = data['total_qty']
            sheet[row][3].value = data['item__product__price']
            sheet[row][4].value = data['total_amount']
            row += 1

    book.save('report.xlsx')

    return items
