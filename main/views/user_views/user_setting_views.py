import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.role.base_role.selectors import get_all_base_roles_by_author
from main.services.role.selectors import get_role_by_id
from main.services.user.selectors import get_app_user_by_token


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsView(View):
    def get(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)

            if need_user.authority == 1:
                roles = get_all_base_roles_by_author(author=need_user)

                serialized_data = serialize('python', roles)

                instance_output_list_of_dicts = []
                for role in serialized_data:
                    id = role['pk']
                    fields_dict = role['fields']
                    fields_dict['id'] = id

                    if fields_dict['percentage'] is None:
                        instance_output_list_of_dicts.append({'id': id,
                                                              'name': fields_dict['name'],
                                                              'description': fields_dict['description'],
                                                              'color': fields_dict['color'],
                                                              'amount': fields_dict['amount'],
                                                              'type': fields_dict['type']
                                                              })

                    if fields_dict['amount'] is None:
                        instance_output_list_of_dicts.append({'id': id,
                                                              'name': fields_dict['name'],
                                                              'description': fields_dict['description'],
                                                              'color': fields_dict['color'],
                                                              'percentage': fields_dict['percentage'],
                                                              'type': fields_dict['type']
                                                              })
                roles_dict = {
                    "roles": instance_output_list_of_dicts
                }

                output_data = roles_dict

                return JsonResponse(output_data, status=200)
            else:
                output_data = {'roles': {}}

                return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def post(self, request):
        token = get_token(request)
        author = get_app_user_by_token(token=token)

        if author:
            if author.authority == 1:
                post_body = json.loads(request.body)

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
                        'author': author,
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
                        'author': author,
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
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class UserViewForIndexInEnd(View):
    def patch(self, request, role_id):
        token = get_token(request)

        user = get_app_user_by_token(token=token)
        if user:
            role_instance = get_role_by_id(role_id=role_id)

            if role_instance:
                if role_instance.author == user:
                    patch_body = json.loads(request.body)
                    name = patch_body.get('name')
                    description = patch_body.get('description')
                    color = patch_body.get('color')
                    percentage = patch_body.get('percentage')
                    amount = patch_body.get('amount')

                    if name is not None:
                        if role_instance.is_base:
                            return JsonResponse(FORBIDDEN_CHANGE_BASE_ROLE_NAME, status=404)

                        else:
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
                            'description': role_instance.description,
                            'color': role_instance.color,
                            'percentage': role_instance.percentage,
                            'type': role_instance.type
                        }
                        return JsonResponse(data, status=200)

                    if role_instance.amount is not None:
                        data = {
                            'id': role_instance.id,
                            'name': role_instance.name,
                            'description': role_instance.description,
                            'color': role_instance.color,
                            'amount': role_instance.amount,
                            'type': role_instance.type
                        }
                        return JsonResponse(data, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def delete(self, request, role_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            role_to_delete = get_role_by_id(role_id=role_id)
            if role_to_delete:

                if role_to_delete.author == user:
                    role_to_delete.delete()

                    return JsonResponse(DELETE_SUCCESS_DATA, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
