from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('depoimentos/', views.depoimentos, name='depoimentos'),
    path('contato/', views.contato, name='contato'),
]

