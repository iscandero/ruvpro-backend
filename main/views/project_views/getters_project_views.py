from django.core.serializers import serialize
from django.db.models import Sum
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.serv_info import SERV_NAME
from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.project.selectors import get_projects_by_owner, get_project_by_id
from main.services.user.selectors import get_app_user_by_token
from main.services.worker.selectors import get_workers_by_project
from main.views.template_paginate_view import ViewPaginatorMixin


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsWithPaginateView(ViewPaginatorMixin, View):
    def get(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        flag_short = request.headers['short']

        if user:
            projects = get_projects_by_owner(owner_project=user)

            serialized_data = serialize('python', projects)

            instance_output_list_of_dicts = []

            if flag_short == 'True':
                for project in serialized_data:
                    project_id = project['pk']
                    fields_task_dict = project['fields']
                    instance_output_list_of_dicts.append({'id': project_id,
                                                          'name': fields_task_dict['name']
                                                          })
            else:
                for project in serialized_data:
                    project_id = project['pk']
                    fields_task_dict = project['fields']
                    instance_output_list_of_dicts.append({'id': project_id,
                                                          'name': fields_task_dict['name'],
                                                          'budget': fields_task_dict['budget'],
                                                          'isArchived': fields_task_dict['is_archived'],
                                                          'workTime': fields_task_dict['work_time'],
                                                          'averageRate': fields_task_dict['average_rate']
                                                          })

            page_number = int(request.headers['X-Pagination-Current-Page'])

            count_in_page = int(request.headers['X-Pagination-Per-Page'])

            return JsonResponse(self.paginate(instance_output_list_of_dicts, page_number, count_in_page, 'projects'),
                                status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsView(View):
    def get(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        flag_short = request.headers['short']

        if user:
            projects = get_projects_by_owner(owner_project=user)

            serialized_data = serialize('python', projects)

            instance_output_list_of_dicts = []

            if flag_short == 'True':
                for project in serialized_data:
                    project_id = project['pk']
                    fields_task_dict = project['fields']
                    instance_output_list_of_dicts.append({'id': project_id,
                                                          'name': fields_task_dict['name']
                                                          })
            else:
                for project in serialized_data:
                    project_id = project['pk']
                    fields_task_dict = project['fields']
                    instance_output_list_of_dicts.append({'id': project_id,
                                                          'name': fields_task_dict['name'],
                                                          'budget': fields_task_dict['budget'],
                                                          'isArchived': fields_task_dict['is_archived'],
                                                          'workTime': fields_task_dict['work_time'],
                                                          'averageRate': fields_task_dict['average_rate']
                                                          })

            output_data = {
                "projects": instance_output_list_of_dicts
            }

            return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectView(View):
    def get(self, request, project_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            project = get_project_by_id(project_id=project_id)
            if project:
                if project.owner == user:
                    employees_list = get_workers_by_project(project=project)

                    serialized_data = serialize('python', employees_list)

                    instance_output_list_of_dicts = []
                    for employee in serialized_data:
                        fields_dict = employee['fields']
                        id = employee['pk']

                        time_emp_on_prj = TimeEntry.objects.filter(employee_id=id).aggregate(Sum('work_time')),
                        work_time = 0 if time_emp_on_prj[0]['work_time__sum'] is None else time_emp_on_prj[0][
                            'work_time__sum']

                        user = AppUser.objects.get(id=fields_dict['user'])
                        avatar = None if not user.avatar else SERV_NAME + str(user.avatar.url)

                        instance_output_list_of_dicts.append({
                            'id': id,
                            'userId': fields_dict['user'],
                            'rate': fields_dict['rate'],
                            'advance': fields_dict['advance'],
                            'role': fields_dict['role'],
                            'salary': fields_dict['salary'],
                            'work_time': work_time,
                            'avatar': avatar,
                            'project': project_id
                        })

                    output_data = {
                        'id': project.id,
                        'name': project.name,
                        'workers': instance_output_list_of_dicts,
                        'budget': project.budget,
                        'isArchived': project.is_archived,
                        'workTime': project.work_time,
                        'averageRate': project.average_rate,
                    }

                    return JsonResponse(output_data, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)
            else:
                return JsonResponse(PROJECT_NOT_FOUND_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
