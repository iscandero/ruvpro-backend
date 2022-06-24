from django.urls import path

from main.views import authorizationsViews



urlpatterns = [
    path('api/user/login', authorizationsViews.UserLogin.as_view()),
    path('api/user/signup', authorizationsViews.UserRegistry.as_view()),
    path('api/user/send-code', authorizationsViews.UserSendCode.as_view()),
    path('api/user/token-renew', authorizationsViews.UserRenewToken.as_view()),
    path('api/user/token-renew', authorizationsViews.UserRenewToken.as_view()),


]
