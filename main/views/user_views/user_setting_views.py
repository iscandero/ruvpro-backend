import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.role.base_role.use_cases import get_pretty_view_base_roles_by_user
from main.services.role.selectors import get_role_by_id
from main.services.role.use_cases import get_role_output_data
from main.services.user.selectors import get_app_user_by_token


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsView(View):
    def get(self, request):
        token = get_token(request)
        if AppUser.objects.filter(token_data=token):
            need_user = AppUser.objects.get(token_data=token)

            if need_user.authority == 1:

                instance_output_list_of_dicts = get_pretty_view_base_roles_by_user(user=need_user)

                output_data = {
                    "roles": instance_output_list_of_dicts
                }

                return JsonResponse(output_data, status=200)
            else:

                return JsonResponse(USER_NOT_A_SUB_DATA, status=400)

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
                    output_data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'percentage': new_role.percentage,
                    }
                    return JsonResponse(output_data, status=200)

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
                    output_data = {
                        'id': new_role.id,
                        'name': new_role.name,
                        'description': new_role.description,
                        'color': new_role.color,
                        'amount': new_role.amount,
                        'type': new_role.type
                    }
                    return JsonResponse(output_data, status=200)

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

                    update_fields = []
                    if name is not None:
                        role_instance.name = name
                        update_fields.append('name')

                    if description is not None:
                        role_instance.description = description
                        update_fields.append('description')

                    if color is not None:
                        role_instance.color = color
                        update_fields.append('color')

                    if percentage is not None and amount is not None:
                        return JsonResponse(DUPLICATION_AMOUNT_PERCENTAGE_DATA, status=404)

                    elif percentage is not None and amount is None:
                        if role_instance.amount is not None:
                            role_instance.amount = None
                        role_instance.percentage = percentage
                        update_fields.append('amount')
                        update_fields.append('percentage')

                    elif amount is not None and percentage is None:
                        if role_instance.percentage is not None:
                            role_instance.percentage = None
                        role_instance.amount = amount
                        update_fields.append('amount')
                        update_fields.append('percentage')

                    role_instance.save(update_fields=update_fields)

                    output_data = get_role_output_data(role=role_instance)

                    return JsonResponse(output_data, status=200)

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
