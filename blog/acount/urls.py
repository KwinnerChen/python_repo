from django.urls import path
from acount import views
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView, PasswordResetCompleteView,
                                      PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView)


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_def, name='logout'),
    path('register/', views.register, name='register'),
    path('change_password/', PasswordChangeView.as_view(), name='password_change'),
    path('change_password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]