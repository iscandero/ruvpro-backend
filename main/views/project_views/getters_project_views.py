import json

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
from main.services.role.project_role.selectors import get_roles_by_project
from main.services.role.selectors import get_role_by_id
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_worker
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

            instance_output_list_of_dicts = []
            if flag_short == 'True':
                for project in projects:
                    instance_output_list_of_dicts.append({'id': project.id,
                                                          'name': project.name
                                                          })
            else:
                for project in projects:
                    instance_output_list_of_dicts.append({'id': project.id,
                                                          'name': project.name,
                                                          'budget': project.budget,
                                                          'isArchived': project.id,
                                                          'workTime': project.work_time,
                                                          'averageRate': project.average_rate
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

            instance_output_list_of_dicts = []

            if flag_short == 'True':
                for project in projects:
                    instance_output_list_of_dicts.append({'id': project.id,
                                                          'name': project.name
                                                          })
            else:
                for project in projects:
                    instance_output_list_of_dicts.append({'id': project.id,
                                                          'name': project.name,
                                                          'budget': project.budget,
                                                          'isArchived': project.id,
                                                          'workTime': project.work_time,
                                                          'averageRate': project.average_rate
                                                          })

            output_data = {
                "projects": instance_output_list_of_dicts
            }

            return JsonResponse(output_data, status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    def get(self, request, project_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            project = get_project_by_id(project_id=project_id)
            if project:
                if project.owner == user:
                    employees_list = get_workers_by_project(project=project)

                    workers_output_list_of_dicts = []
                    for employee in employees_list:
                        time_emp_on_prj = TimeEntry.objects.filter(employee_id=employee.id).aggregate(Sum('work_time')),
                        work_time = 0 if time_emp_on_prj[0]['work_time__sum'] is None else time_emp_on_prj[0][
                            'work_time__sum']

                        user = get_app_user_by_worker(worker=employee)
                        avatar = None if not user.avatar else SERV_NAME + str(user.avatar.url)

                        workers_output_list_of_dicts.append({
                            'id': employee.id,
                            'userId': employee.user_id,
                            'rate': employee.rate,
                            'advance': employee.advance,
                            'role_id': employee.role_id,
                            'roleName': employee.role.name,
                            'roleColor': employee.role.color,
                            'salary': employee.salary,
                            'work_time': work_time,
                            'avatar': avatar,
                            'project_id': project_id
                        })

                    project_roles = get_roles_by_project(project=project)

                    roles_output_list_of_dicts = []
                    for role in project_roles:
                        if role.percentage is not None:
                            roles_output_list_of_dicts.append({
                                'id': role.id,
                                'name': role.name,
                                'description': role.description,
                                'color': role.color,
                                'percentage': role.percentage,
                                'type': role.type
                            })
                        else:
                            roles_output_list_of_dicts.append({
                                'id': role.id,
                                'name': role.name,
                                'description': role.description,
                                'color': role.color,
                                'amount': role.amount,
                                'type': role.type
                            })

                    output_data = {
                        'id': project.id,
                        'name': project.name,
                        'workers': workers_output_list_of_dicts,
                        'roles': roles_output_list_of_dicts,
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

    def patch(self, request, project_id):
        patch_body = json.loads(request.body)

        name = patch_body.get('name')
        budget = patch_body.get('budget')
        roles = patch_body.get('roles')

        project = get_project_by_id(project_id=project_id)

        update_fields = []
        if name is not None:
            project.name = name
            update_fields.append('name')

        if budget is not None:
            project.budget = budget
            update_fields.append('budget')

        project.save(update_fields=update_fields)

        if roles is not None:
            for role_from_body in roles:
                id_role_for_change = role_from_body['id']
                role_for_change = get_role_by_id(role_id=id_role_for_change)

                if role_for_change:
                    role_for_change.description = role_from_body['description']
                    role_for_change.color = role_from_body['color']

                    if 'percentage' in role_from_body is not None:
                        role_for_change.percentage = role_from_body['percentage']

                    if 'amount' in role_from_body is not None:
                        role_for_change.amount = role_from_body['amount']

                    role_for_change.save()

                else:
                    return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

        employees = get_workers_by_project(project=project)

        workers_output_list_of_dicts = []
        for worker in employees:
            avatar = None if not worker.user.avatar else SERV_NAME + str(worker.user.avatar.url)
            workers_output_list_of_dicts.append({'id': worker.id,
                                                 'userId': worker.user_id,
                                                 'rate': worker.rate,
                                                 'advance': worker.advance,
                                                 'role_id': worker.role_id,
                                                 'roleName': worker.role.name,
                                                 'roleColor': worker.role.color,
                                                 'salary': 0,
                                                 'work_time': 0,
                                                 'avatar': avatar,
                                                 'name': worker.user.name,
                                                 'project_id': worker.project_id,
                                                 })

        project_roles = get_roles_by_project(project=project)

        roles_output_list_of_dicts = []
        for role in project_roles:
            if role.percentage is not None:
                roles_output_list_of_dicts.append({
                    'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'color': role.color,
                    'percentage': role.percentage,
                    'type': role.type
                })
            else:
                roles_output_list_of_dicts.append({
                    'id': role.id,
                    'name': role.name,
                    'description': role.description,
                    'color': role.color,
                    'amount': role.amount,
                    'type': role.type
                })

        output_data = {
            'id': project.id,
            'name': project.name,
            'workers': workers_output_list_of_dicts,
            'roles': roles_output_list_of_dicts,
            'budget': project.budget,
            'isArchived': project.is_archived,
            'workTime': project.work_time,
            'averageRate': project.average_rate,
        }

        return JsonResponse(output_data, status=201)
