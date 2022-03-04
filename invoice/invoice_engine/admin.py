from django.contrib import admin
from .models import Contract, Invoice, Product, InvoiceItem

# Register your models here.
admin.site.register(Contract)
admin.site.register(Invoice)
admin.site.register(Product)
admin.site.register(InvoiceItem)
