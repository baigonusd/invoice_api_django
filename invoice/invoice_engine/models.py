from django.db import models
from django.conf import settings
from datetime import date

User = settings.AUTH_USER_MODEL


class Contract(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contracts', blank=False)
    title = models.CharField(max_length=50, db_index=True)


class Product(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Invoice(models.Model):
    # Number - invoice number -> Invoice #123
    number = models.IntegerField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='invoices', blank=False)
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, blank=False)
    date = models.DateField(default=date.today)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = gen_slug(self.title)
    #         self.sum = self.price * self.number
    #     super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='item', blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=False)
    qty = models.DecimalField(max_digits=6, decimal_places=2)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    # def get_sum(self):
    #     sum = self.qty * self.price
    #     return sum
