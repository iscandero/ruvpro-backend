import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.models import *
from main.parsers import *

from main.const_data.template_errors import *


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
                'message': 'Введён неккоректный код'
            }
            return JsonResponse(data, status=404)


class UserLogin(View):
    def post(self, request):
        post_body = json.loads(request.body)

        phone = post_body.get('phone')
        password = post_body.get('pin')

        # дальше че-то от Вани
        # найти по номеру юзера и дать ему токен, который пришлёт Ваня


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsView(View):
    def get(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)
            if need_user.authority == 1:
                roles = Role.objects.filter(author_id=need_user)

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
                output_data = {'settings': {}}

                return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)

    def post(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            if User.objects.get(token_data=token).authority == 1:
                post_body = json.loads(request.body)

                author_id = User.objects.get(token_data=token)

                name = post_body.get('name')
                description = post_body.get('description')
                color = post_body.get('color')
                percentage = post_body.get('percentage')
                amount = post_body.get('amount')

                if percentage is not None and amount is not None:
                    return JsonResponse(DUPLICATION_AMOUNT_PERCENTAGE_DATA, status=404)

                elif percentage is not None and amount is None:
                    data_to_create = {
                        'name': name,
                        'description': description,
                        'color': color,
                        'percentage': percentage,
                        'amount': None,
                        'author_id': author_id
                    }
                    new_role = Role.objects.create(**data_to_create)
                    data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'percentage': new_role.percentage,
                    }
                    return JsonResponse(data, status=200)

                elif amount is not None and percentage is None:
                    data_to_create = {
                        'name': name,
                        'description': description,
                        'color': color,
                        'percentage': None,
                        'amount': amount,
                        'author_id': author_id,
                    }
                    new_role = Role.objects.create(**data_to_create)
                    data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'amount': new_role.amount,
                    }
                    return JsonResponse(data, status=200)

            else:
                return JsonResponse(USER_NOT_A_SUB_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def patch(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)

            patch_body = json.loads(request.body)
            name = patch_body.get('name')
            email = patch_body.get('email')
            phone = patch_body.get('phone')
            avatar = patch_body.get('avatar')
            bio = patch_body.get('bio')
            authority = patch_body.get('authority')

            social_list = patch_body.get('social')

            if social_list is not None:
                for i in range(len(social_list)):
                    name = social_list[i]['name']
                    url = social_list[i]['url']

                    social_network = SocialNetwork.objects.get(name=name)

                    if not Social.objects.filter(user_id=need_user, social_network_id=social_network):
                        Social.objects.create(user_id=need_user, social_network_id=social_network, url=url)
                    else:
                        social_instance = Social.objects.get(user_id=need_user, social_network_id=social_network)
                        social_instance.url = url
                        social_instance.save(update_fields=['url'])
            if name is not None:
                need_user.name = name
                need_user.save(update_fields=['name'])

            if email is not None:
                if not User.objects.filter(email=email):
                    need_user.email = email
                    need_user.save(update_fields=['email'])

                else:
                    return JsonResponse(USER_EXIST_EMAIL, status=404)

            if phone is not None:
                if not User.objects.filter(phone=phone):
                    need_user.phone = phone
                    need_user.save(update_fields=['phone'])
                else:
                    return JsonResponse(USER_EXIST_PHONE, status=404)

            # РАЗОБРАТЬСЯ
            if avatar is not None:
                need_user.avatar = avatar
                need_user.save(update_fields=['avatar'])

            if bio is not None:
                need_user.bio = bio
                need_user.save(update_fields=['bio'])

            if authority is not None:
                need_user.authority = authority
                need_user.save(update_fields=['authority'])

            socials_user = Social.objects.filter(user_id=need_user)

            serialized_data = serialize('python', socials_user)

            count_of_instance = socials_user.count()

            instance_output_list_of_dicts = list(dict())
            for i in range(count_of_instance):
                fields_dict = serialized_data[i]['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network_id']).name,
                    'url': fields_dict['url']

                })

            avatar = None if not need_user.avatar else str(need_user.avatar.url)

            data = {
                'id': need_user.id,
                'name': need_user.name,
                'email': need_user.email,
                'phone': need_user.phone,
                'avatar': avatar,
                'bio': need_user.bio,
                'social': instance_output_list_of_dicts,
                'authority': need_user.authority
            }
            return JsonResponse(data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)

    def delete(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            User.objects.get(token_data=token).delete()

            return JsonResponse(DELETE_SUCCESS_DATA, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)

    def get(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)

            avatar = None if not need_user.avatar else str(need_user.avatar.url)

            socials_user = Social.objects.filter(user_id=need_user)

            serialized_data = serialize('python', socials_user)

            count_of_instance = socials_user.count()

            instance_output_list_of_dicts = list(dict())
            for i in range(count_of_instance):
                fields_dict = serialized_data[i]['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network_id']).name,
                    'url': fields_dict['url']

                })

            data = {
                'id': need_user.id,
                'name': need_user.name,
                'email': need_user.email,
                'phone': need_user.phone,
                'avatar': avatar,
                'bio': need_user.bio,
                'social': instance_output_list_of_dicts,
                'authority': need_user.authority,
            }

            return JsonResponse(data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserViewForIndexInEnd(View):
    def patch(self, request, role_id):
        if Role.objects.filter(id=role_id):
            role_instance = Role.objects.get(id=role_id)

            patch_body = json.loads(request.body)
            name = patch_body.get('name')
            description = patch_body.get('description')
            color = patch_body.get('color')
            percentage = patch_body.get('percentage')
            amount = patch_body.get('amount')

            if name is not None:
                role_instance.name = name
                role_instance.save(update_fields=['name'])

            if description is not None:
                role_instance.description = description
                role_instance.save(update_fields=['description'])

            if color is not None:
                role_instance.color = color
                role_instance.save(update_fields=['color'])

            if percentage is not None and amount is not None:
                return JsonResponse(DUPLICATION_AMOUNT_PERCENTAGE_DATA, status=404)

            elif percentage is not None and amount is None:
                if role_instance.amount is not None:
                    role_instance.amount = None
                role_instance.percentage = percentage
                role_instance.save(update_fields=['amount', 'percentage'])

            elif amount is not None and percentage is None:
                if role_instance.percentage is not None:
                    role_instance.percentage = None
                role_instance.amount = amount
                role_instance.save(update_fields=['amount', 'percentage'])

            if role_instance.percentage is not None:
                data = {
                    'id': role_instance.id,
                    'name': role_instance.name,
                    'color': role_instance.color,
                    'percentage': role_instance.percentage
                }
                return JsonResponse(data, status=200)

            if role_instance.amount is not None:
                data = {
                    'id': role_instance.id,
                    'name': role_instance.name,
                    'color': role_instance.color,
                    'amount': role_instance.amount
                }
                return JsonResponse(data, status=200)


        else:
            return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

    def delete(self, request, role_id):
        if Role.objects.filter(id=role_id):
            Role.objects.get(id=role_id).delete()

            return JsonResponse(DELETE_SUCCESS_DATA, status=200)

        else:
            return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class LogOutView(View):
    def post(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)
            need_user.token_data = None
            need_user.save(update_fields=['token_data'])
            return JsonResponse(SUCCESS_LOGOUT, status=200)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePhone(View):
    def post(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            need_user = User.objects.get(token_data=token)
            patch_body = json.loads(request.body)
            phone = patch_body.get('phone')

            if not User.objects.filter(phone=phone):
                need_user.phone = phone
                need_user.save(update_fields=['phone'])
                return JsonResponse(SUCCESS_CHANGE_PHONE, status=200)
            else:
                return JsonResponse(USER_EXIST_PHONE, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)
