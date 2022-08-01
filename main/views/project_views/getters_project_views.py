import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.const_data.template_errors import *
from main.models import Project
from main.pagination import ProjectPagination
from main.parsers import *
from main.serializers.project_serializers.project_serializers import ProjectSerializer
from main.services.project.selectors import get_project_by_id
from main.services.project.use_cases import get_full_output_project_data, get_short_output_projects_by_owner, \
    get_long_output_projects_by_owner, get_long_output_projects_by_owner__full
from main.services.role.selectors import get_role_by_id
from main.services.role.use_cases import get_pretty_view_roles_by_project
from main.services.user.selectors import get_app_user_by_token
from main.services.worker.use_cases import get_pretty_view_workers_by_project
from main.views.template_paginate_view import ViewPaginatorMixin


class GetProjectsWithPaginateView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination

# @method_decorator(csrf_exempt, name='dispatch')
# class GetProjectsWithPaginateView(ViewPaginatorMixin, View):
#     def get(self, request):
#         token = get_token(request)
#         user = get_app_user_by_token(token=token)
#         flag_short = request.headers['short'] if 'short' in request.headers else 'false'
#         flag_archived = request.headers['isArchived'] if 'isArchived' in request.headers else 'false'
#
#         if user:
#             if flag_short == 'true':
#                 instance_output_list_of_dicts = get_short_output_projects_by_owner(owner=user, archived=flag_archived)
#             else:
#                 instance_output_list_of_dicts = get_long_output_projects_by_owner__full(owner=user,
#                                                                                         archived=flag_archived)
#
#             page_number = int(request.headers['X-Pagination-Current-Page'])
#             count_in_page = int(request.headers['X-Pagination-Per-Page'])
#
#             return JsonResponse(self.paginate(instance_output_list_of_dicts, page_number, count_in_page, 'projects'),
#                                 status=200)
#
#         else:
#             return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsView(View):
    def get(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        flag_short = request.headers['short'] if 'short' in request.headers else 'false'
        flag_archived = request.headers['isArchived'] if 'isArchived' in request.headers else 'false'

        if user:
            if flag_short == 'true':
                instance_output_list_of_dicts = get_short_output_projects_by_owner(owner=user, archived=flag_archived)
            else:
                instance_output_list_of_dicts = get_long_output_projects_by_owner__full(owner=user,
                                                                                        archived=flag_archived)
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

                    workers_output_list_of_dicts = get_pretty_view_workers_by_project(project=project)

                    roles_output_list_of_dicts = get_pretty_view_roles_by_project(project=project)

                    output_data = get_full_output_project_data(project=project, workers=workers_output_list_of_dicts,
                                                               roles=roles_output_list_of_dicts)

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
        currency = patch_body.get('currency')

        project = get_project_by_id(project_id=project_id)

        update_fields = []
        if name is not None:
            project.name = name
            update_fields.append('name')

        if budget is not None:
            project.budget = budget
            project.save(update_fields=['budget'])

        if currency is not None:
            project.currency = currency
            update_fields.append('currency')

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

        workers_output_list_of_dicts = get_pretty_view_workers_by_project(project=project)

        roles_output_list_of_dicts = get_pretty_view_roles_by_project(project=project)

        output_data = get_full_output_project_data(project=project, workers=workers_output_list_of_dicts,
                                                   roles=roles_output_list_of_dicts)

        return JsonResponse(output_data, status=200)
