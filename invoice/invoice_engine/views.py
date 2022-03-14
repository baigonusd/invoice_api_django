import json

from django.shortcuts import render
from django.conf import settings
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import User
from invoice_engine.utils import save_save
from .models import Invoice, Contract, Product, InvoiceItem
from .serializers import ContractSerializer, InvoiceSerializer, ProductSerializer, InvoiceItemSerializer, ListOfInvoicesSerializer
from .permissions import *
from .tasks import email


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
    # @action(detail=False, methods=['get'])
    # def get_mail_xlsx(self, request, *args, **kwargs):
    #     queryset = InvoiceItem.objects.filter(invoice=request.data["invoice"])
    #     save_file(queryset)
    #     email.delay(request.user.email)
    #     return Response()

    # authorized as admin, mounth (exp: 3)
    @action(detail=False, methods=['get'])
    def returning_response(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            try:
                b = save_save(self, request, *args, **kwargs)
            except Exception as e:
                return Response({"ERROR": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            email.delay(request.user.email)
            return Response(b)
        else:
            return Response({"ERROR": "You're not admin"}, status=status.HTTP_403_FORBIDDEN)

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
