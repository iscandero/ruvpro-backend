import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.project.selectors import get_project_by_id
from main.services.project.use_cases import get_full_output_project_data
from main.services.role.project_role.selectors import get_role_by_name_and_author_and_project
from main.services.role.use_cases import get_pretty_view_roles_by_project
from main.services.user.selectors import get_app_user_by_token, get_app_user_by_id

from main.services.worker.use_cases import get_pretty_view_workers_by_project


@method_decorator(csrf_exempt, name='dispatch')
class SetCompleteProjectView(View):
    def put(self, request, project_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            project = get_project_by_id(project_id=project_id)
            if project:
                if project.owner == user:
                    put_body = json.loads(request.body)
                    is_archived = put_body.get('isArchived')
                    project.is_archived = is_archived
                    project.save(update_fields=['is_archived'])
                    return JsonResponse(SUCCESS_DATA, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)
            else:
                return JsonResponse(PROJECT_NOT_FOUND_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    def post(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        if user:
            if user.authority == 1:
                post_body = json.loads(request.body)
                name = post_body.get('name')
                roles_list = post_body.get('roles')
                workers_list = post_body.get('workers')
                budget = post_body.get('budget')
                project = Project.objects.create(name=name, budget=budget, is_archived=False, owner=user)

                roles = []
                for role_from_body in roles_list:
                    role_from_body['project'] = project
                    role_from_body['is_base'] = False
                    role_from_body['author'] = user
                    roles.append(Role.objects.create(**role_from_body))

                for worker in workers_list:
                    current_user = get_app_user_by_id(id=worker['userId'])
                    role = get_role_by_name_and_author_and_project(name=worker['roleName'], author=user,
                                                                   project=project)
                    data_to_create_employee = {
                        'user': current_user,
                        'project': project,
                        'advance': worker['advance'],
                        'role': role
                    }
                    ProjectEmployee.objects.create(**data_to_create_employee)

                workers_output_list_of_dicts = get_pretty_view_workers_by_project(project=project)

                roles_output_list_of_dicts = get_pretty_view_roles_by_project(project=project)

                output_data = get_full_output_project_data(project=project, workers=workers_output_list_of_dicts,
                                                           roles=roles_output_list_of_dicts)

                return JsonResponse(output_data, status=201)

            else:
                return JsonResponse(USER_NOT_A_SUB_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)
