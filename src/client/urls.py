from django.urls import path
from . import views

app_name = 'client'
urlpatterns = [
    path('list/', views.ClientListView.as_view(), name='list'),
    path('update/<int:pk>/', views.ClientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
