from django.urls import path
from . import views

app_name = 'info'
urlpatterns = [
    path('<int:pk>/', views.InfoUpdateView.as_view(), name='update'),
]
