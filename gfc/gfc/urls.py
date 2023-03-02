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
    path(
        'categories/<str:search_name>/',
        views.category_list_view,
        name='categories_list'),
    path(
        'categories/',
        views.category_list_redirect,
        name='categories_list_redirect'),
    path(
        'groups/<str:search_name>/',
        views.all_groups_view,
        name='all_groups'),
    path(
        'groups/',
        views.all_groups_redirect,
        name='all_groups_redirect'),
    path(
        'add_monetary_account/',
        views.add_monetary_account_view,
        name="add_monetary_account"),
    path(
        'view_accounts/',
        views.view_user_pot_accounts,
        name='view_accounts'),
    path(
        'create_category/',
        views.create_category_view,
        name="create_category"),
    path(
        'add_transaction/',
        views.add_transaction_view,
        name='add_transaction'),
    path(
        'edit_transaction/<int:pk>',
        views.edit_transaction_view,
        name='edit_transaction'),
    path(
        'delete_transaction/<int:pk>',
        views.delete_transaction_view,
        name='delete_transaction'),
    path(
        'view_transactions/<str:filter_type>',
        views.view_users_transactions,
        name="view_transactions"),
    path(
        'edit_user_details/',
        views.edit_user_details_view,
        name="edit_user_details"),
    path('profile/', views.profile_view, name="profile"),
    path('delete_profile/', views.delete_profile_view, name="delete_profile"),
    path(
        'view_transactions/',
        views.view_users_transactions_redirect,
        name="view_transactions_redirect"),
    path(
        'change_password/',
        views.change_password_view,
        name="change_password"),
    path(
        'create_target/category/<int:pk>',
        views.create_category_target_view,
        name="create_category_target"),
    path(
        'create_target/user/',
        views.create_user_target_view,
        name="create_user_target"),
    path(
        'create_target/account/<int:pk>',
        views.create_account_target_view,
        name="create_account_target"),
    path(
        'edit_target/category/<int:pk>',
        views.edit_category_target_view,
        name="edit_category_target"),
    path(
        'edit_target/account/<int:pk>',
        views.edit_account_target_view,
        name="edit_account_target"),
    path(
        'edit_target/user/<int:pk>',
        views.edit_user_target_view,
        name="edit_user_target"),
    path(
        'delete_target/category/<int:pk>',
        views.delete_category_target_view,
        name="delete_category_target"),
    path(
        'delete_target/account/<int:pk>',
        views.delete_account_target_view,
        name="delete_account_target"),
    path(
        'delete_target/user/<int:pk>',
        views.delete_user_target_view,
        name="delete_user_target"),
    path(
        'edit_category/<int:pk>',
        views.edit_category_view,
        name="edit_category"),
    path(
        'delete_category/<int:pk>',
        views.delete_category_view,
        name="delete_category"),
    path(
        'create_user_group/',
        views.create_user_group_view,
        name="create_user_group"),
    path(
        'delete_user_group/<int:pk>',
        views.delete_user_group_view,
        name="delete_user_group"),
    path(
        'edit_user_group/<int:pk>',
        views.edit_user_group_view,
        name='edit_user_group'),
    path(
        'join_user_group/',
        views.join_user_group_view,
        name="join_user_group"),
    path(
        'remove_user_from_user_group/<int:group_pk>/<int:user_pk>',
        views.remove_user_from_user_group_view,
        name="remove_user_from_user_group"),
    path(
        'make_owner_of_user_group/<int:group_pk>/<int:user_pk>',
        views.make_owner_of_user_group_view,
        name="make_owner_of_user_group"),
    path(
        'add_user_to_user_group/<int:group_pk>',
        views.add_user_to_user_group_view,
        name="add_user_to_user_group"),
    path(
        'reset_password',
        PasswordResetView.as_view(
            template_name="pages/email/password_reset.html"),
        name='password_reset'),
    path(
        'reset_password/done',
        PasswordResetDoneView.as_view(
            template_name="pages/email/password_reset_done.html"),
        name='password_reset_done'),
    path(
        'reset_password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/',
        PasswordResetConfirmView.as_view(
            template_name="pages/email/password_reset_confirm.html"),
        name='password_reset_confirm'),
    path(
        'reset_password/complete/',
        PasswordResetCompleteView.as_view(
            template_name="pages/email/password_reset_complete.html"),
        name='password_reset_complete'),
    path(
        'view_savings_accounts/',
        views.view_savings_accounts,
        name='view_savings_accounts'),
    re_path(
        'individual_account/(?P<pk>\\d+)/(?P<filter_type>\\w+)/$',
        views.individual_account_view,
        name="individual_account"
    ),
    re_path(
        'filter_transaction_request/(?P<redirect_name>\\w+)/$',
        views.filter_transaction_request,
        name="filter_transaction_request"
    ),
    re_path(
        'filter_transaction_request_with_pk/(?P<redirect_name>\\w+)/(?P<pk>\\d+)/$',
        views.filter_transaction_request_with_pk,
        name="filter_transaction_request_with_pk"
    ),
    re_path(
        'individual_account/(?P<pk>\\d+)/$',
        views.individual_account_redirect,
        name="individual_account_redirect"
    ),
    re_path(
        'edit_monetary_account/(?P<pk>\\d+)/$',
        views.edit_monetary_account_view,
        name="edit_monetary_account"
    ),
    re_path(
        'delete_monetary_account/(?P<pk>\\d+)/$',
        views.delete_monetary_account_view,
        name="delete_monetary_account"
    ),
    re_path(
        'individual_category/(?P<pk>\\d+)/(?P<filter_type>\\w+)/$',
        views.individual_category_view,
        name="individual_category"
    ),
    re_path(
        'individual_category/(?P<pk>\\d+)/$',
        views.individual_category_redirect,
        name="individual_category_redirect"
    ),
    re_path(
        'individual_transaction/(?P<pk>\\d+)/$',
        views.individual_transaction_view,
        name="individual_transaction"
    ),
    path('quiz/', views.quiz_view, name='quiz'),
    re_path(
        'quiz/(?P<question_total>\\d+)/(?P<sort_type>\\w+)/$',
        views.quiz_view,
        name="quiz_with_params"
    ),
    re_path(
        'quiz_ready/(?P<question_total>\\d+)/$',
        views.quiz_ready_view,
        name="quiz_ready"
    ),
    re_path(
        'quiz_questions/(?P<pk>\\d+)/$',
        views.quiz_question_view,
        name="quiz_questions"
    ),
    re_path(
        'quiz_score/(?P<pk>\\d+)/$',
        views.quiz_score_view,
        name="quiz_score"
    ),
    re_path(
        'individual_group/(?P<pk>\\d+)/$',
        views.individual_group_view,
        name="individual_group"
    ),
    path('add_transactions_via_bank_statement/',
         views.add_transactions_via_bank_statement,
         name='add_transactions_via_bank_statement'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
