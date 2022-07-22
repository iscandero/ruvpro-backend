from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.parsers import *
from main.services.team.selectors import get_team_by_owner, is_user_in_team
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_id


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserByTeam(View):
    def delete(self, request, user_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            if user.authority == 1:
                team = get_team_by_owner(owner=user)
                user_to_delete = get_app_user_by_id(id=user_id)
                if is_user_in_team(user=user_to_delete, team=team):
                    if user_to_delete != user:
                        team.participants.remove(user_to_delete)
                        return JsonResponse(DELETE_SUCCESS_DATA, status=200)
                    else:
                        return JsonResponse(NOT_DELETE_DATA, status=403)
                else:
                    return JsonResponse(USER_NOT_EXIST_IN_TEAM_DATA, status=404)
            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
