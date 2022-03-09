from rest_framework import generics, viewsets
from django.shortcuts import render
from django.http import HttpResponse
import json
from invoice_engine.utils import save_file, save_report, save_save
from .models import Invoice, Contract, Product, InvoiceItem
from .serializers import ContractSerializer, InvoiceSerializer, ProductSerializer, InvoiceItemSerializer, ListOfInvoicesSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import *
from django.conf import settings
# from drf_excel.mixins import XLSXFileMixin
# from drf_excel.renderers import XLSXRenderer
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import email
from django.db.models import Sum
from core.models import User


def main_page(request):
    return render(request, 'invoice_engine/index.html')


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ContractViewSet(viewsets.ModelViewSet):
    #queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Contract.objects.filter(user=self.request.user)
        else:
            return None


class InvoiceViewSet(viewsets.ModelViewSet):
    # queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Invoice.objects.filter(user=self.request.user)
        else:
            return None

    # @action(detail=False, methods=['get'])
    # def get_mail_xslx(self, request, *args, **kwargs):
    #     queryset = Invoice.objects.filter(user=request.user)
    #     save_file(queryset)
    #     email.delay(request.user.email)
    #     return Response()


class InvoiceItemViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return InvoiceItem.objects.filter(invoice=self.request.data["invoice"])
        else:
            return None

    # body = invoice.id (exp: 1)
    @action(detail=False, methods=['get'])
    def get_mail_xlsx(self, request, *args, **kwargs):
        queryset = InvoiceItem.objects.filter(invoice=request.data["invoice"])
        save_file(queryset)
        email.delay(request.user.email)
        return Response()

    # authorized as admin, mounth (exp: 3)
    @action(detail=False, methods=['get'])
    def returning_response(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            users = User.objects.all()
            # json: [{user1: [{data1},...]}, {user2}: [{data2},...] ]
            b = [{users[i].email: list(InvoiceItem.objects.values('product__title', 'price').filter(
                invoice__user__id=i+1, invoice__date__gte=f'2022-0{request.data["month"]}-01', invoice__date__lt=f'2022-0{int(request.data["month"])+1}-01').annotate(total_qty=Sum('qty')).annotate(total_amount=Sum('amount')))} for i in range(len(users))]
            # save_report(b)
            save_save(b)
            email.delay(request.user.email)
            return Response(b)
        else:
            return Response({"ERROR": "You're not authorized"})

# month_lt = f'2022-0{int(request.data["month"])+1}-01'
# month_gte = f'2022-0{request.data["month"]}-01'

# class CreateXlsxViewSet(viewsets.ModelViewSet):
#     serializer_class = InvoiceItemSerializer
#     queryset = InvoiceItem.objects.all()


# class ListOf

# class XlsxSendToEmailViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = EmailSerializer
#     renderer_classes = (XLSXRenderer,)
#     filename = 'othcet.xlsx'
# permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
