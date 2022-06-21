import json

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
        # need_user = User.objects.get(token_data=token)
        #
        # task_serialized_data = serialize('python', tasks)
        #
        # count_of_instance = Task.objects.count()
        #
        # instance_output_list_of_dicts = list(dict())
        # for i in range(count_of_instance):
        #     task_id = task_serialized_data[i]['pk']
        #     fields_task_dict = task_serialized_data[i]['fields']
        #     fields_task_dict['task_id'] = task_id
        #     instance_output_list_of_dicts.append({'task_id': task_id,
        #                                           'task_name': fields_task_dict['task_name'],
        #                                           'task_description': fields_task_dict['task_description'],
        #                                           'task_status': fields_task_dict['task_status'],
        #                                           'folder_id': fields_task_dict['folder_id']
        #                                           })

        output_data = {
            "token": token_data_with_bearer
        }

        return JsonResponse(output_data, safe=False)
