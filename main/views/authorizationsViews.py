import json

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.models import *
from main.parsers import *

BASE_URL = 'https://api.therun.app'


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistry(View):
    def post(self, request):
        post_body = json.loads(request.body)

        email = post_body.get('email')
        phone = post_body.get('phone')
        code = post_body.get('code')
        password = post_body.get('pin')
        name = post_body.get('name')

        user_data_for_api = {
            'email': email,
            'phone': phone,
            'code': code,
            'pin': password,
            'firstname': name,
        }

        response = requests.post(f"{BASE_URL}/api/user/signup", json=user_data_for_api)
        json_resp = response.json()

        if response.status_code == 200:
            data_to_create_user = {
                'token_data': json_resp.get('token'),
                'name': name,
                'email': email,
                'phone': phone,
            }

            User.objects.create(**data_to_create_user)

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
        response = requests.post(f"{BASE_URL}/api/user/login", json=data_to_api)
        json_resp = response.json()
        token = json_resp.get('token')
        user = User.objects.get(phone=phone)
        user.token_data = token
        user.save(update_fields=['token_data'])

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserSendCode(View):
    def post(self, request):
        post_body = json.loads(request.body)
        phone = post_body.get('phone')
        type = post_body.get('type')
        sms = post_body.get('sms')

        data_to_api = {
            'phone': phone,
            'type': type,
            'sms': sms,
        }

        response = requests.post(f"{BASE_URL}/api/user/send-code", json=data_to_api)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserRenewToken(View):
    def post(self, request):
        post_body = json.loads(request.body)

        refreshToken = post_body.get('refreshToken')

        data_to_api = {
            'refreshToken': refreshToken,
        }

        user = User.objects.get(token_data=refreshToken)

        response = requests.post(f"{BASE_URL}/api/user/token-renew", json=data_to_api)
        json_resp = response.json()

        if response.status_code == 200:
            user.token_data = json_resp.get('token')

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class UserCheckCode(View):
    def post(self, request):
        post_body = json.loads(request.body)

        phone = post_body.get('phone')
        code = post_body.get('code')
        type = post_body.get('type')

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
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)
            need_user.token_data = None
            need_user.save(update_fields=['token_data'])

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        response = requests.post(f"{BASE_URL}/api/user/logout", headers=headers)
        json_resp = response.json()

        return JsonResponse(json_resp, status=response.status_code)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePinView(View):
    def post(self, request):
        token = get_token(request)
        post_body = json.loads(request.body)

        pin = post_body.get('pin')

        data_to_api = {
            'pin': pin
        }

        headers = {
            "Authorization": "Bearer " + str(token)
        }

        response = requests.post(f"{BASE_URL}/api/user/logout", json=data_to_api, headers=headers)
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