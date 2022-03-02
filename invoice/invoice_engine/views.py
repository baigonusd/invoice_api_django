from rest_framework import generics, viewsets
from django.shortcuts import render
import json
from invoice_engine.utils import save_file
from .models import Invoice, Contract
from .serializers import ContractSerializer, InvoiceSerializer
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


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(detail=False, methods=['get'])
    def get_mail_xslx(self, request, *args, **kwargs):
        queryset = Invoice.objects.filter(user=request.user)
        save_file(queryset)
        email.delay(request.user.email)
        return Response()


# class XlsxSendToEmailViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
#     queryset = Invoice.objects.all()
#     serializer_class = EmailSerializer
#     renderer_classes = (XLSXRenderer,)
#     filename = 'othcet.xlsx'
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
