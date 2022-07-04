from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.parsers import *
from main.services.social.use_cases import get_social_output_list_by_user
from main.services.team.selectors import get_team_by_owner
from main.services.user.selectors import get_app_user_by_token
from main.services.user.use_cases import get_app_user_output_data_with_social_list


@method_decorator(csrf_exempt, name='dispatch')
class GetUsersByTeam(View):
    def get(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            if user.authority == 1:
                team = get_team_by_owner(owner=user)
                output_list = []
                for participant in team.participants:
                    social_list = get_social_output_list_by_user(user=participant.user)
                    output_list.append(
                        get_app_user_output_data_with_social_list(user=participant.user, social_list=social_list))

                output_data = {
                    "teammates": output_list
                }

                return JsonResponse(output_data, status=200)
            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
