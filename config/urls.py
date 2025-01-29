
from django.contrib import admin
from django.urls import include, path
from gimnasio.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('gimnasio.urls')), 
]
