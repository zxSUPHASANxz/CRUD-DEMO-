"""
URL configuration for theone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as acc
from mechanics import views as mec
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name="home"),

    # Accounts
    path('login/', acc.login_view, name='login'),
    path('logout/', acc.logout_view, name='logout'),
    path('register/', acc.register_view, name='register'),
    path('register/success/', acc.register_success, name='register_success'),

    # Mechanics CRUD
    path('mechanics/', mec.mechanic_list, name='mechanic_list'),
    path('mechanics/create/', mec.mechanic_create, name='mechanic_create'),
    path('mechanics/<int:pk>/edit/', mec.mechanic_edit, name='mechanic_edit'),
    path('mechanics/<int:pk>/delete/', mec.mechanic_delete, name='mechanic_delete'),

    # Password reset (Django built-in auth views)
    path('password_reset/', include('django.contrib.auth.urls')),
    
    # admin dashboard
    path('admin-dashboard/', acc.admin_dashboard, name="admin_dashboard"),
    path('admin-dashboard/user/<int:user_id>/delete/', acc.delete_user, name="delete_user"),


    # Update user (admin)
    path('admin-dashboard/user/<int:user_id>/update/', acc.update_user, name="update_user"),
    # Update mechanic (admin)
    path('admin-dashboard/mechanic/<int:mechanic_id>/update/', acc.update_mechanic, name="update_mechanic"),
    path('admin-dashboard/mechanic/<int:mechanic_id>/delete/', acc.delete_mechanic, name="delete_mechanic"),

]
