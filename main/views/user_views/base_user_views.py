import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.social.selectors import get_socials_by_user
from main.services.user.selectors import get_app_user_by_token, is_exist_user_phone, get_avatar_path


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def patch(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            patch_body = json.loads(request.body)
            name = patch_body.get('name')
            email = patch_body.get('email')
            phone = patch_body.get('phone')
            bio = patch_body.get('bio')
            authority = patch_body.get('authority')

            social_list = patch_body.get('social')

            if social_list is not None:
                for i in range(len(social_list)):
                    name_social = social_list[i]['name']
                    url = social_list[i]['url']

                    social_network = SocialNetwork.objects.get(name=name_social)

                    if not Social.objects.filter(user=need_user, social_network=social_network):
                        Social.objects.create(user=need_user, social_network=social_network, url=url)

                    else:
                        social_instance = Social.objects.get(user=need_user, social_network=social_network)
                        social_instance.url = url
                        social_instance.save(update_fields=['url'])

            fields_to_update = []

            if name is not None:
                need_user.name = name
                fields_to_update.append('name')

            if email is not None:
                if not AppUser.objects.filter(email=email):
                    need_user.email = email
                    fields_to_update.append('email')

                else:
                    if need_user.email != email:
                        return JsonResponse(USER_EXIST_EMAIL, status=404)

            if phone is not None:
                if not AppUser.objects.filter(phone=phone):
                    need_user.phone = phone
                    fields_to_update.append('phone')
                else:
                    return JsonResponse(USER_EXIST_PHONE, status=404)

            if bio is not None:
                need_user.bio = bio
                fields_to_update.append('bio')

            if authority is not None:
                need_user.authority = authority

                # Так, чтобы сработал корректно триггер
                need_user.save(update_fields=['authority'])

            need_user.save(update_fields=fields_to_update)

            socials_user = Social.objects.filter(user=need_user)

            serialized_data = serialize('python', socials_user)

            instance_output_list_of_dicts = []
            for social_network in serialized_data:
                fields_dict = social_network['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network']).name,
                    'url': fields_dict['url']

                })

            avatar = get_avatar_path(user=need_user)

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
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def delete(self, request):
        token = get_token(request)
        user_to_delete = get_app_user_by_token(token=token)

        if user_to_delete:
            user_to_delete.delete()
            return JsonResponse(DELETE_SUCCESS_DATA, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)

    def get(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)

        if need_user:
            avatar = get_avatar_path(user=need_user)
            socials_user = get_socials_by_user(user=need_user)

            serialized_data = serialize('python', socials_user)

            instance_output_list_of_dicts = []
            for social_user in serialized_data:
                fields_dict = social_user['fields']

                instance_output_list_of_dicts.append({
                    'name': SocialNetwork.objects.get(id=fields_dict['social_network']).name,
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
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePhoneView(View):
    def post(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            post_body = json.loads(request.body)
            phone = post_body.get('phone')

            if need_user.phone == phone:
                return JsonResponse(SUCCESS_CHANGE_PHONE, status=200)

            if not is_exist_user_phone(phone=phone):
                need_user.phone = phone
                need_user.save(update_fields=['phone'])
                return JsonResponse(SUCCESS_CHANGE_PHONE, status=200)

            else:
                return JsonResponse(USER_EXIST_PHONE, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
