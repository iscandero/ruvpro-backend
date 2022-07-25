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
from main.services.work_with_date import convert_timestamp_to_date
from main.services.worker.selectors import get_worker_by_id, get_worker_by_user_role_project
from main.services.worker.use_cases import get_worker_output_data, get_full_worker_output_data, get_rate_by_worker


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

                if role_id is not None:
                    role = get_role_by_id(role_id=role_id)

                    if role:
                        worker.role = role
                        worker.save(update_fields=['role'])

                    else:
                        return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

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
    def post(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            post_body = json.loads(request.body)
            times = post_body.get('times')

            output_list = []
            for time in times:
                current_employee = get_worker_by_id(worker_id=time['workerId'])
                if current_employee:
                    date = convert_timestamp_to_date(time['date'])
                    amount_advance = time['advance']
                    advance = HistoryAdvance.objects.create(date=date, employee=current_employee,
                                                            advance=amount_advance)

                    current_user = current_employee.user
                    avatar = get_avatar_path(user=current_user)

                    output_list.append({
                        'id': current_employee.id,
                        'userId': current_user.id,
                        'rate': get_rate_by_worker(worker=current_employee),
                        'advance': current_employee.advance,
                        'roleId': current_employee.role.id,
                        'salary': current_employee.salary,
                        'workTime': current_employee.work_time * 3600,
                        'avatar': avatar,
                        'name': current_user.name,
                        'projectId': current_employee.project.id,
                        'roleName': current_employee.role.name,
                        'roleColor': current_employee.role.color,
                    })

            output_data = {
                'workers': output_list
            }
            return JsonResponse(output_data, status=200)

        return JsonResponse(NO_PERMISSION_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class TimeEntryView(View):
    def post(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            post_body = json.loads(request.body)
            times = post_body.get('times')

            output_list = []
            for time in times:
                current_employee = get_worker_by_id(worker_id=time['workerId'])
                if current_employee:
                    date = convert_timestamp_to_date(time['date'])
                    work_time = time['workTime'] / 3600
                    time_entry = TimeEntry.objects.create(date=date, work_time=work_time, employee=current_employee,
                                                          initiator=user)

                    current_user = current_employee.user
                    avatar = get_avatar_path(user=current_user)

                    output_list.append({
                        'id': current_employee.id,
                        'userId': current_user.id,
                        'rate': get_rate_by_worker(worker=current_employee),
                        'advance': current_employee.advance,
                        'roleId': current_employee.role.id,
                        'salary': current_employee.salary,
                        'workTime': current_employee.work_time * 3600,
                        'avatar': avatar,
                        'name': current_user.name,
                        'projectId': current_employee.project.id,
                        'roleName': current_employee.role.name,
                        'roleColor': current_employee.role.color,
                    })

            output_data = {
                'workers': output_list
            }
            return JsonResponse(output_data, status=200)

        return JsonResponse(NO_PERMISSION_DATA, status=404)
