from django.urls import path, include

from main.views.user_views import base_user_views, upload_avatar_view, user_setting_views

urlpatterns = [
    path('api/', include([
        path('user', base_user_views.UserView.as_view()),
        path('user/settings', user_setting_views.SettingsAPIView.as_view()),
        path('user/settings/<int:role_id>', user_setting_views.UserViewForIndexInEnd.as_view()),
        path('user/settings/currency', user_setting_views.UserSettingsCurrencyView.as_view()),
        path('file/upload', upload_avatar_view.UploadAvatar.as_view()),
    ]))
]
