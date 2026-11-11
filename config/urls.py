
from django.contrib import admin
from django.urls import path
from accounts.views import register_page, login_page, home_page, logout_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
]
