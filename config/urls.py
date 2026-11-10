from django.contrib import admin
from django.urls import path
from accounts.views import register_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_page, name='register'),
]
