from rest_framework import generics, viewsets
from django.shortcuts import render
from .models import Invoice, Contract
from .serializers import ContractSerializer, InvoiceSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import *
from django.conf import settings


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
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
