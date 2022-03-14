import openpyxl
import datetime

from core.models import User
from invoice_engine.models import InvoiceItem
from django.db.models import Sum


def save_save(self, request, *args, **kwargs):
    users = User.objects.all()
    month_value = int(request.query_params.get('month'))
    items = []
    if month_value is None:
        return {"ERROR": "Month can't be None"}

    date_gte = datetime.date(year=2022, month=month_value, day=1)
    if 0 < month_value < 12:
        date_lt = datetime.date(year=2022, month=month_value+1, day=1)
    elif month_value == 12:
        date_lt = datetime.date(year=2023, month=1, day=1)
    else:
        return {'ERROR': 'Month need to be between 1 and 12 inclusive'}

    for i in range(len(users)):
        user_items = list(InvoiceItem.objects.values('product__title', 'product__price')
                          .filter(invoice__user__id=i+1, invoice__date__gte=date_gte, invoice__date__lt=date_lt)
                          .annotate(total_qty=Sum('qty'))
                          .annotate(total_amount=Sum('amount'))
                          )
        if user_items:
            items.append({users[i].email: user_items})

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

            sheet[row][1].value = data['product__title']
            sheet[row][2].value = data['total_qty']
            sheet[row][3].value = data['product__price']
            sheet[row][4].value = data['total_amount']
            row += 1

    book.save('report.xlsx')

    return items
