import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import USER_NOT_FOUND_DATA, SUCCESS_DATA
from main.models import AppUser, Team
from main.parsers import get_token
from main.services.social.use_cases import get_social_output_list_by_user
from main.services.team.selectors import get_team_by_owner
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_email
from main.services.user.use_cases import get_app_user_output_data_with_social_list, get_short_user_output_data, \
    get_no_register_user_output_data


@method_decorator(csrf_exempt, name='dispatch')
class AddUserToTeam(View):
    def post(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            post_body = json.loads(request.body)
            name = post_body.get('name')
            email = post_body.get('email')

            team = get_team_by_owner(owner=user)
            user_to_add = get_app_user_by_email(email=email)

            if user_to_add:
                if user_to_add.id in team.participants.values_list('id', flat=True):
                    return JsonResponse(SUCCESS_DATA, status=200)

                else:
                    team.participants.add(user_to_add)
                    social_list = get_social_output_list_by_user(user=user_to_add)
                    output_data = get_app_user_output_data_with_social_list(user=user_to_add, social_list=social_list)
                    return JsonResponse(output_data, status=200)
            else:
                non_register_user = AppUser.objects.create(name=name, email=email, is_register=False, authority=0)
                team.participants.add(non_register_user)

                output_data = get_no_register_user_output_data(user=non_register_user)
                return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
