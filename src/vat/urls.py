from django.urls import path
from . import views

app_name = 'vat'
urlpatterns = [
    path('list/',                      views.VatListView.as_view(),   name='list'),
    path('create/<int:year>/<int:q>/', views.VatCreateView.as_view(), name='create'),
]
