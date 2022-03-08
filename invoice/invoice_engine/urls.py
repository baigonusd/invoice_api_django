from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'contract', ContractViewSet, basename='contract')
router.register(r'invoice', InvoiceViewSet, basename='invoice')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'invoice_item', InvoiceItemViewSet, basename='invoice_item'),
# router.register(r'create_xlsx', CreateXlsxViewSet, basename='create_xlsx')

# router.register(r'xlsx', XlsxSendToEmailViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('test_orm/', test_orm),
]
