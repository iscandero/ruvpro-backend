import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.views import View

from .models import *


class UserRegistry(View):
    def post(self, request):
        post_body = json.loads(request.body)

        name = post_body.get('firstname')
        phone = post_body.get('phone')
        code = post_body.get('code')
        email = post_body.get('email')
        password = post_body.get('pin')  # пока на всякий случай

        if code == 1:  # 1 - убрать, тут, то че дал Ваня
            token = 1  # от Вани
            validUntil = 1  # от Вани
            status = 1  # от Вани
            refreshToken = 1  # от Вани
            user_data = {
                'token_data': token,
                'name': name,
                'phone': phone,
                'email': email
            }
            user_object = User.objects.create(**user_data)
            data = {
                'token': token,
                'validUntil': validUntil,
                'status': status,
                'refreshToken': refreshToken
            }
        else:
            data = {
                'message': 'Error in  authentication code'
            }
            return JsonResponse(data, status=404)


class UserLogin(View):
    def post(self, request):
        post_body = json.loads(request.body)

        phone = post_body.get('phone')
        password = post_body.get('pin')

        # дальше че-то от Вани
        # найти по номеру юзера и дать ему токен, который пришлёт Ваня


class UserView(View):
    def get(self, request):
        token_data_with_bearer = request.headers['Authorization']
        token = str(token_data_with_bearer)[7:]  # по нему найти юзера
        need_user = User.objects.get(token_data=token)
        if need_user.authority == 1:
            roles = Role.objects.filter(author_id=need_user)
            id = need_user.id

            serialized_data = serialize('python', roles)

            count_of_instance = roles.count()

            instance_output_list_of_dicts = list(dict())
            for i in range(count_of_instance):

                id = serialized_data[i]['pk']
                fields_dict = serialized_data[i]['fields']
                fields_dict['id'] = id

                if fields_dict['percentage'] is None:
                    instance_output_list_of_dicts.append({'id': id,
                                                          'name': fields_dict['name'],
                                                          'description': fields_dict['description'],
                                                          'color': fields_dict['color'],
                                                          'amount': fields_dict['amount']
                                                          })

                if fields_dict['amount'] is None:
                    instance_output_list_of_dicts.append({'id': id,
                                                          'name': fields_dict['name'],
                                                          'description': fields_dict['description'],
                                                          'color': fields_dict['color'],
                                                          'percentage': fields_dict['percentage']
                                                          })
            roles_dict = {
                "roles": instance_output_list_of_dicts
            }

            output_data = {'settings': roles_dict}

            return JsonResponse(output_data, status=200)
        else:
            data = {
                'message': 'User has not subscription'
            }
            return JsonResponse(data, status=404)
