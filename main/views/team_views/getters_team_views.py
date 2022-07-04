from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.parsers import *
from main.services.project.use_cases import get_output_projects_by_member_and_owner
from main.services.social.use_cases import get_social_output_list_by_user
from main.services.team.selectors import get_team_by_owner, is_user_in_team
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_id
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
                participants = team.participants.all()
                if participants is not None:
                    for participant in participants:
                        social_list = get_social_output_list_by_user(user=participant)
                        output_list.append(
                            get_app_user_output_data_with_social_list(user=participant, social_list=social_list))

                output_data = {
                    "teammates": output_list
                }

                return JsonResponse(output_data, status=200)

            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsByTeamUser(View):
    def get(self, request, user_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            if user.authority == 1:
                need_to_view_user = get_app_user_by_id(id=user_id)
                if need_to_view_user:
                    team = get_team_by_owner(owner=user)
                    if is_user_in_team(user=need_to_view_user, team=team):

                        output_data = {
                            "projects": get_output_projects_by_member_and_owner(member=need_to_view_user, owner=user)
                        }

                        return JsonResponse(output_data, status=200)

                    else:
                        return JsonResponse(USER_NOT_EXIST_IN_TEAM_DATA, status=404)
                else:
                    return JsonResponse(USER_NOT_FOUND_DATA, status=404)

            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
