from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',          include('board.urls')),
    path('info/',     include('info.urls')),
    path('in/',       include('income.urls')),
    path('out/',      include('out.urls')),
    path('client/',   include('client.urls')),
    path('vat/',      include('vat.urls')),
    path('costtype/', include('costtype.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
