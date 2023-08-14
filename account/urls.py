from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# app_name = 'account'
# post views here

urlpatterns = [
    # path('login/', views.user_login, name='login') -previous login view
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password url
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Django also provides the authentication URL patterns that you just created.
    path('', include('django.contrib.auth.urls')),

    path('register/', views.register, name='register'),
    path('edit_form', views.edit_form, name='edit_form'),

    path('users/', views.user_list,  name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]


# You can get more information about the built-in authentication views at
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#allauthentication-views.

# You can see the authentication URL patterns included at
# https://github.com/django/django/blob/stable/3.0.x/django/contrib/auth/urls.py

