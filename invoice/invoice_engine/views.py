from rest_framework import generics, viewsets
from django.shortcuts import render
import json
from invoice_engine.utils import save_file
from .models import Invoice, Contract, Product, InvoiceItem
from .serializers import ContractSerializer, InvoiceSerializer, ProductSerializer, InvoiceItemSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import *
from django.conf import settings
# from drf_excel.mixins import XLSXFileMixin
# from drf_excel.renderers import XLSXRenderer
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .tasks import email


def main_page(request):
    return render(request, 'invoice_engine/index.html')


# class ContractAPIView(generics.ListCreateAPIView):
#     queryset = Contract.objects.all()
#     serializer_class = ContractSerializer

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

    @action(detail=False, methods=['get'])
    def get_mail_xlsx(self, request, *args, **kwargs):
        queryset = InvoiceItem.objects.filter(invoice=request.data["invoice"])
        save_file(queryset)
        email.delay(request.user.email)
        return Response()

    # class XlsxSendToEmailViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    #     queryset = Invoice.objects.all()
    #     serializer_class = EmailSerializer
    #     renderer_classes = (XLSXRenderer,)
    #     filename = 'othcet.xlsx'
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
