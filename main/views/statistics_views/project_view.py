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
class GetProjectStatistic(View):
    def get(self, request):
        pass
        # token = get_token(request)
        # user = get_app_user_by_token(token=token)
