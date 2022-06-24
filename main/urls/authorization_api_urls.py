from django.urls import path

from main.views import authorizationsViews

urlpatterns = [
    path('api/user/login', authorizationsViews.UserLogin.as_view()),
    path('api/user/signup', authorizationsViews.UserRegistry.as_view()),
    path('api/user/send-code', authorizationsViews.UserSendCode.as_view()),
    path('api/user/token-renew', authorizationsViews.UserRenewToken.as_view()),
    path('api/user/check-code', authorizationsViews.UserCheckCode.as_view()),
    path('api/user/logout', authorizationsViews.LogOutView.as_view()),
    path('api/user/change-pin', authorizationsViews.ChangePinView.as_view()),
    path('api/user/reset-pin', authorizationsViews.ResetPinView.as_view()),
]
