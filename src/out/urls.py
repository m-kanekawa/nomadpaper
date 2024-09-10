from django.urls import path
from . import views

app_name = 'out'
urlpatterns = [
    path('list/', views.OutListView.as_view(), name='list'),
    path('update/<int:pk>/', views.OutUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
