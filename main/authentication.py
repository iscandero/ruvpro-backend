from rest_framework import authentication, exceptions, status
from rest_framework.response import Response

from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.models import AppUser
from main.parsers import get_token
from main.services.user.selectors import get_app_user_by_token


class AppUserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = get_token(request)
        if token is None:
            return None

        user = get_app_user_by_token(token=token)
        request.user = user

        return user, None
