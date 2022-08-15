import json

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.models import *
from main.parsers import *
from main.services.auth.selectors import get_auth_data_by_refresh_token
from main.services.user.selectors import get_no_register_app_user_by_email, get_deleted_app_user_by_phone, \
    get_app_user_by_phone
from main.services.work_with_date import convert_timestamp_to_date

BASE_URL = 'http://82.148.18.226'


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistry(View):
    def post(self, request):
        post_body = json.loads(request.body)

        email = post_body.get('email')
        phone = post_body.get('phone')
        password = post_body.get('pin')
        name = post_body.get('name')
        code = post_body.get('code')

        find_user = get_deleted_app_user_by_phone(phone=phone)
        if find_user:
            find_user.email = email
            find_user.name = name
            find_user.is_deleted = False
            find_user.is_register = True
            find_user.save()

            data_to_api = {
                'pin': password,
                'code': code,
                'phone': phone
            }

            requests.post(f"{BASE_URL}/api/user/reset-pin", json=data_to_api)

            response = requests.post(f"{BASE_URL}/api/user/login", json=data_to_api)
            json_resp = response.json()

            if response.status_code == 200:
                token = json_resp.get('token')
                refresh_token = json_resp.get('refreshToken')
                valid_until = json_resp.get('validUntil')

                AuthData.objects.create(user=find_user, token_data=token, refresh_token_data=refresh_token,
                                        valid_until=convert_timestamp_to_date(valid_until))
                json_resp['code'] = 66
            return JsonResponse(json_resp, status=response.status_code)

        else:

            user_data_for_api = {
                'email': email,
                'phone': phone,
                'code': code,
                'pin': password,
                'firstname': name,
                'username': phone
            }

            response = requests.post(f"{BASE_URL}/api/user/signup", json=user_data_for_api)
            json_resp = response.json()

            if response.status_code == 200:
                token = json_resp.get('token')
                refresh_token = json_resp.get('refreshToken')
                valid_until = json_resp.get('validUntil')

                user_to_create_or_update = get_no_register_app_user_by_email(email=email)

                if not user_to_create_or_update:
                    data_to_create_user = {
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'is_register': True,
                        'authority': 0,
                    }
                    user_to_create_or_update = AppUser.objects.create(**data_to_create_user)

                else:
                    user_to_create_or_update.name = name
                    user_to_create_or_update.phone = phone
                    user_to_create_or_update.authority = 0
                    user_to_create_or_update.is_register = True
                    user_to_create_or_update.save(update_fields=['name', 'phone'])

                AuthData.objects.create(user=user_to_create_or_update, token_data=token,
                                        refresh_token_data=refresh_token,
                                        valid_until=convert_timestamp_to_date(valid_until))

            return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(View):
    def post(self, request):
        post_body = json.loads(request.body)
        phone = post_body.get('phone')
        password = post_body.get('pin')
        data_to_api = {
            'pin': password,
            'phone': phone
        }

        user = get_app_user_by_phone(phone=phone)

        if not user.is_deleted:
            response = requests.post(f"{BASE_URL}/api/user/login", json=data_to_api)
            json_resp = response.json()

            if response.status_code == 200:
                token = json_resp.get('token')
                refresh_token = json_resp.get('refreshToken')
                valid_until = json_resp.get('validUntil')

                AuthData.objects.create(user=user, token_data=token, refresh_token_data=refresh_token,
                                        valid_until=convert_timestamp_to_date(valid_until))

            return JsonResponse(json_resp, status=response.status_code)

        else:
            output_data = {
                "errors": "Phone number or password entered incorrectly",
                "code": 3004,
                "extended_desc": "Phone number or password entered incorrectly",
                "status": False
            }
            return JsonResponse(output_data, status=403)


@method_decorator(csrf_exempt, name='dispatch')
class UserSendCode(View):
    def post(self, request):
        post_body = json.loads(request.body)
        phone = post_body.get('phone')
        type = post_body.get('type')
        target = post_body.get('target')

        find_user = get_deleted_app_user_by_phone(phone=phone)
        if find_user:
            type = 1

        data_to_api = {
            'phone': phone,
            'type': type,
            'target': target,
        }

        response = requests.post(f"{BASE_URL}/api/user/send-code", json=data_to_api)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserRenewToken(View):
    def post(self, request):
        post_body = json.loads(request.body)
        token = get_token(request)

        refresh_token = post_body.get('refreshToken')

        data_to_api = {
            'refreshToken': refresh_token,
        }

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        auth_data_to_change = get_auth_data_by_refresh_token(refresh=refresh_token)

        if auth_data_to_change:
            response = requests.post(f"{BASE_URL}/api/user/token-renew", json=data_to_api, headers=headers)
            json_resp = response.json()

            if response.status_code == 200:
                auth_data_to_change.token_data = json_resp.get('token')
                auth_data_to_change.refresh_token_data = json_resp.get('refreshToken')
                auth_data_to_change.valid_until = convert_timestamp_to_date(json_resp.get('validUntil'))

                auth_data_to_change.save(update_fields=['token_data', 'refresh_token_data', 'valid_until'])

            return JsonResponse(json_resp, status=response.status_code)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=403)


@method_decorator(csrf_exempt, name='dispatch')
class UserCheckCode(View):
    def post(self, request):
        post_body = json.loads(request.body)

        phone = post_body.get('phone')
        code = post_body.get('code')
        type = post_body.get('type')

        find_user = get_deleted_app_user_by_phone(phone=phone)

        if find_user:
            type = 1

        data_to_api = {
            "phone": phone,
            "code": code,
            "type": type,
        }

        response = requests.post(f"{BASE_URL}/api/user/check-code", json=data_to_api)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class LogOutView(View):
    def post(self, request):
        token = get_token(request)

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        response = requests.post(f"{BASE_URL}/api/user/logout", headers=headers)

        AuthData.objects.get(token_data=token).delete()

        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePinView(View):
    def post(self, request):
        token = get_token(request)
        post_body = json.loads(request.body)

        old_pin = post_body.get('oldPin')
        pin = post_body.get('pin')

        data_to_api = {
            'oldPin': old_pin,
            'pin': pin
        }

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        response = requests.post(f"{BASE_URL}/api/user/change-pin", json=data_to_api, headers=headers)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class ResetPinView(View):
    def post(self, request):
        post_body = json.loads(request.body)

        pin = post_body.get('pin')
        code = post_body.get('code')
        phone = post_body.get('phone')

        data_to_api = {
            "pin": pin,
            "code": code,
            "phone": phone,
        }

        response = requests.post(f"{BASE_URL}/api/user/reset-pin", json=data_to_api)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)
