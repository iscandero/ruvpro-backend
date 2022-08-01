import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.parsers import *
from main.services.history_workers.selectors import get_workers_history_by_workers_ids_and_date_interval
from main.services.project.use_cases import get_output_projects_by_member_and_owner
from main.services.team.selectors import get_team_by_owner, is_user_in_team
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_id
from main.services.user.use_cases import get_app_user_output_data_with_social_list
from main.services.work_with_date import convert_timestamp_to_date
from main.services.worker.selectors import get_workers_by_user_ids_list_and_owner_projects
from main.services.worker.use_cases import get_worker_output_data_for_statistic


@method_decorator(csrf_exempt, name='dispatch')
class GetWorkerStatistic(View):
    def get(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        if user:
            post_body = json.loads(request.body)
            user_ids_list = post_body.get('userIds')
            start_date = convert_timestamp_to_date(post_body.get('startDate'))
            end_date = convert_timestamp_to_date(post_body.get('endDate'))

            workers_ids = get_workers_by_user_ids_list_and_owner_projects(user_ids_list=user_ids_list,
                                                                          owner_projects=user)

            workers_history = get_workers_history_by_workers_ids_and_date_interval(workers_ids=workers_ids,
                                                                                   start_date=start_date,
                                                                                   end_date=end_date)

            history_instances_list = []
            if workers_history is not None:
                for worker_history in workers_history:
                    history_instances_list.append(
                        {
                            'id': worker_history.id,
                            'date': worker_history.date_change,
                            'worker': get_worker_output_data_for_statistic(worker=worker_history.employee,
                                                                           income=worker_history.salary,
                                                                           work_time=worker_history.work_time,
                                                                           rate=worker_history.rate),
                        }
                    )
            output_data = {
                "workerStatistics": history_instances_list
            }
            return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
