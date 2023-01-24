"""gfc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path

from financial_companion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('log_in/', views.log_in_view, name='log_in'),
    path('log_out/', views.log_out_view, name='log_out'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add_monetary_account', views.add_monetary_account_view, name="add_monetary_account"),
    path('categories/', views.category_list_view, name='categories_list'),
    re_path(
        'edit_monetary_account/(?P<account_type>\w+)/(?P<pk>\d+)/$',
        views.edit_monetary_account_view,
        name="edit_monetary_account"
    ),
]
