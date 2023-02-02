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
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from financial_companion import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('log_in/', views.log_in_view, name='log_in'),
    path('log_out/', views.log_out_view, name='log_out'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('categories/<str:search_name>/', views.category_list_view, name='categories_list'),
    path('categories/', views.category_list_redirect, name='categories_list_redirect'),
    path('add_monetary_account/', views.add_monetary_account_view, name="add_monetary_account"),
    path('view_accounts/', views.view_user_pot_accounts, name='view_accounts'),
    path('create_category/', views.create_category_view, name="create_category"),
    path('view_transactions/<str:filter_type>', views.view_users_transactions, name="view_transactions"),
    path('edit_user_details/', views.edit_user_details_view, name="edit_user_details"),
    path('view_transactions/', views.view_users_transactions_redirect, name="view_transactions_redirect"),
    path('change_password/', views.change_password_view, name="change_password"),
    path('edit_category/<int:pk>', views.edit_category_view, name = "edit_category"),
    path('delete_category/<int:pk>', views.delete_category_view, name = "delete_category"),
    path('reset_password', PasswordResetView.as_view(template_name="pages/email/password_reset.html"), name='password_reset'),
    path('reset_password/done', PasswordResetDoneView.as_view(template_name="pages/email/password_reset_done.html"), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(template_name="pages/email/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(template_name="pages/email/password_reset_complete.html"), name='password_reset_complete'),
    re_path(
        'individual_account/(?P<pk>\d+)/(?P<filter_type>\w+)/$',
        views.individual_account_view,
        name="individual_account"
    ),
    re_path(
        'filter_transaction_request/(?P<redirect_name>\w+)/$',
        views.filter_transaction_request,
        name="filter_transaction_request"
    ),
    re_path(
        'filter_transaction_request_with_pk/(?P<redirect_name>\w+)/(?P<pk>\d+)/$',
        views.filter_transaction_request_with_pk,
        name="filter_transaction_request_with_pk"
    ),
    re_path(
        'individual_account/(?P<pk>\d+)/$',
        views.individual_account_redirect,
        name="individual_account_redirect"
    ),
    re_path(
        'edit_monetary_account/(?P<pk>\d+)/$',
        views.edit_monetary_account_view,
        name="edit_monetary_account"
    ),
    re_path(
        'delete_monetary_account/(?P<pk>\d+)/$',
        views.delete_monetary_account_view,
        name="delete_monetary_account"
    ),
    re_path(
        'individual_category/(?P<pk>\d+)/(?P<filter_type>\w+)/$',
        views.individual_category_view,
        name="individual_category"
    ),
    re_path(
        'individual_category/(?P<pk>\d+)/$',
        views.individual_category_redirect,
        name="individual_category_redirect"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
