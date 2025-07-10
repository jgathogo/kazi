# datastore/profiles/urls.py
from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('firms/<int:firm_id>/', views.firm_detail, name='firm_detail'),
]