from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'contract', ContractViewSet)
router.register(r'invoice', InvoiceViewSet)
# router.register(r'xlsx', XlsxSendToEmailViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
