import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *
from main.services.project.selectors import get_projects_by_owner, get_project_by_id
from main.services.role.project_role.selectors import get_role_by_name_and_author_and_project, \
    is_user_has_role_in_project
from main.services.role.selectors import get_role_by_id
from main.services.user.selectors import get_app_user_by_token, get_avatar_path
from main.services.worker.selectors import get_worker_by_id, get_worker_by_user_role_project
from main.services.worker.use_cases import get_worker_output_data, get_full_worker_output_data


@method_decorator(csrf_exempt, name='dispatch')
class WorkerViewWithIndexInEnd(View):
    def delete(self, request, worker_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            projects = get_projects_by_owner(owner_project=user)

            worker = get_worker_by_id(worker_id=worker_id)

            project_with_need_worker = None
            for i in projects:
                if worker.project == i:
                    project_with_need_worker = i
                    break

            if project_with_need_worker is not None:
                worker.delete()
                return JsonResponse(DELETE_SUCCESS_DATA, status=200)

            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)

    def patch(self, request, worker_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            worker = get_worker_by_id(worker_id=worker_id)
            project = worker.project

            if project.owner == user:
                post_body = json.loads(request.body)

                role_id = post_body.get('role_id')
                rate = post_body.get('rate')

                if role_id is not None:
                    role = get_role_by_id(role_id=role_id)

                    if role:
                        worker.role = role
                        worker.save(update_fields=['role'])

                    else:
                        return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

                if rate is not None:
                    worker.rate = rate
                    worker.save(update_fields=['rate'])

                output_data = get_worker_output_data(worker)

                return JsonResponse(output_data, status=200)

            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AddWorkerView(View):
    def post(self, request, project_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        if user:
            project = get_project_by_id(project_id=project_id)

            if project:

                if project.owner == user:
                    post_body = json.loads(request.body)

                    user_id = post_body.get('userId')
                    need_user = AppUser.objects.get(id=user_id)
                    advance = post_body.get('advance')
                    role_id = post_body.get('role_id')
                    need_role = get_role_by_id(role_id=role_id)

                    data_to_create = {
                        'user': need_user,
                        'project': project,
                        'advance': advance,
                        'role': need_role

                    }
                    if get_worker_by_user_role_project(user=need_user, role=need_role, project=project):
                        return JsonResponse(EMPLOYEE_IS_EXIST, status=404)

                    else:
                        employee = ProjectEmployee.objects.create(**data_to_create)

                    output_data = get_full_worker_output_data(worker=employee)

                    return JsonResponse(output_data, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(PROJECT_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdvanceView(View):
    def put(self, request):
        put_body = json.loads(request.body)

        id_worker = put_body.get('workerId')
        advance = put_body.get('advance')

        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            worker = get_worker_by_id(worker_id=id_worker)

            if worker:
                if worker.project.owner == user:
                    worker.advance = advance
                    worker.save(update_fields=['advance'])

                    return JsonResponse(SUCCESS_DATA, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(WORKER_NOT_FOUND, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class TimeEntryView(View):
    def post(self, request, project_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            project = get_project_by_id(project_id=project_id)
            owner_project = project.owner
            role_accounting = get_role_by_name_and_author_and_project(name='Журнал учета', author=owner_project,
                                                                      project=project)

            if owner_project == user or is_user_has_role_in_project(user=user, role=role_accounting, project=project):
                post_body = json.loads(request.body)

                date = post_body.get('date')
                work_time = post_body.get('workTime')
                worker_id = post_body.get('worker_id')

                current_employee = get_worker_by_id(worker_id=worker_id)
                if current_employee:
                    time_entry = TimeEntry.objects.create(date=date, work_time=work_time, employee=current_employee,
                                                          initiator=user)
                    current_user = current_employee.user

                    avatar = get_avatar_path(user=current_user)

                    output_data = {
                        'id': time_entry.id,
                        'userId': current_user.name,
                        'rate': current_employee.rate,
                        'advance': current_employee.advance,
                        'role_id': current_employee.role.id,
                        'salary': current_employee.salary,
                        'work_time': time_entry.work_time,
                        'avatar': avatar,
                        'name': current_user.name,
                        'project_id': current_employee.project.id
                    }

                    return JsonResponse(output_data, status=200)

                else:

                    return JsonResponse(WORKER_NOT_FOUND, status=404)

            return JsonResponse(NO_PERMISSION_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)
