from django.utils.text import slugify
from time import time
from django.db import models
from django.contrib.auth.models import User


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Contract(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owners', blank=False)
    title = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)


class Invoice(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users', blank=False)
    slug = models.SlugField()
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name='contracts', blank=False)
    product = models.CharField(max_length=50)
    price = models.IntegerField()
    number = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)
