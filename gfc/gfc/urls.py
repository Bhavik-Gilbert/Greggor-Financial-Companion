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
    path('categories/<str:filter_type>', views.category_list_view, name='categories_list'),
    path('filter_transaction_request/', views.filter_categories_request, name="filter_categories_request"),
    path('add_monetary_account/', views.add_monetary_account_view, name="add_monetary_account"),
    path('view_accounts/', views.view_user_pot_accounts, name='view_accounts'),
    path('create_category/', views.create_category_view, name="create_category"),
    path('filter_transaction_request/', views.filter_transaction_request, name="filter_transaction_request"),
    path('view_transactions/<str:filter_type>', views.view_users_transactions, name="view_transactions"),
    path('edit_category/<int:pk>', views.edit_category_view, name = "edit_category"),
    re_path(
        'edit_monetary_account/(?P<pk>\d+)/$',
        views.edit_monetary_account_view,
        name="edit_monetary_account"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
