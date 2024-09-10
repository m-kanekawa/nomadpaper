from django.urls import path
from . import views

app_name = 'income'
urlpatterns = [
    path('list/',            views.InListView.as_view(),   name='list'),
    path('info/<int:pk>/',   views.InInfoView.as_view(),   name='info'),
    path('status/<int:pk>/', views.InStatusView.as_view(), name='status'),
    path('detail/<int:pk>/', views.InDetailView.as_view(), name='detail'),
    path('pdf/<int:pk>/',    views.to_pdf,                 name='pdf'),
]
