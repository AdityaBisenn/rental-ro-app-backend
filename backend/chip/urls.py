# myproject/myapp/urls.py
from django.urls import path
from .views import ChipConnectionAPI, GetChipTokenAPI, VerifyChipTokenAPI

urlpatterns = [
    path('chip-connection/', ChipConnectionAPI.as_view(), name='chip-connection'),
    path('getChipToken/', GetChipTokenAPI.as_view(), name='getChipToken'),
    path('verifyChipToken/', VerifyChipTokenAPI.as_view(), name='verifyChipToken'),
]
