from django.urls import path
from . import views

app_name = 'costtype'
urlpatterns = [
    path('list/', views.TypeListView.as_view(), name='list'),
    path('update/<int:pk>/', views.TypeUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
