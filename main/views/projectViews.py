import json
import math

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.serv_info import SERV_NAME
from main.const_data.template_errors import *
from main.models import *
from main.parsers import *


class ViewPaginatorMixin(object):
    min_limit = 1
    max_limit = 100

    def paginate(self, object_list, page, limit, **kwargs):
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (TypeError, ValueError):
            page = 1

        try:
            limit = int(limit)
            if limit < self.min_limit:
                limit = self.min_limit
            if limit > self.max_limit:
                limit = self.max_limit
        except (ValueError, TypeError):
            limit = self.max_limit

        paginator = Paginator(object_list, limit)
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        total_count = len(object_list)

        meta = {
            'totalCount': total_count,
            'pageCount': int(math.ceil(total_count / limit)),
            'currentPage': page,
            'perPage': len(objects),
        }

        data = {
            'projects': list(objects),
            'meta': meta

        }
        return data


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsWithPaginateView(ViewPaginatorMixin, View):
    def get(self, request):
        token = get_token(request)
        user = AppUser.objects.filter(token_data=token).first()
        flag_short = request.headers['short']

        if user:
            projects = Project.objects.filter(owner_id=user)

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

            return JsonResponse(self.paginate(instance_output_list_of_dicts, page_number, count_in_page), status=200)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class GetProjectsView(View):
    def get(self, request):
        token = get_token(request)
        user = AppUser.objects.filter(token_data=token).first()
        flag_short = request.headers['short']

        if user:
            projects = Project.objects.filter(owner_id=user)

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
        user = AppUser.objects.filter(token_data=token).first()

        if user:
            project = Project.objects.filter(id=project_id).first()
            if project:
                if project.owner_id == user:
                    employees_list = ProjectEmployee.objects.filter(project_id=project)

                    serialized_data = serialize('python', employees_list)

                    instance_output_list_of_dicts = []
                    for employee in serialized_data:
                        fields_dict = employee['fields']
                        id = employee['pk']

                        time_emp_on_prj = TimeEntry.objects.filter(employee_id_id=id).aggregate(Sum('work_time')),
                        work_time = 0 if time_emp_on_prj[0]['work_time__sum'] is None else time_emp_on_prj[0][
                            'work_time__sum']

                        user = AppUser.objects.get(id=fields_dict['user_id'])
                        avatar = None if not user.avatar else SERV_NAME + str(user.avatar.url)

                        instance_output_list_of_dicts.append({
                            'id': id,
                            'userId': fields_dict['user_id'],
                            'rate': fields_dict['rate'],
                            'advance': fields_dict['advance'],
                            'role_id': fields_dict['role_id'],
                            'salary': fields_dict['salary'],
                            'work_time': work_time,
                            'avatar': avatar,
                            'project_id': project_id
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


@method_decorator(csrf_exempt, name='dispatch')
class SetCompleteProjectView(View):
    def put(self, request, project_id):
        token = get_token(request)
        user = AppUser.objects.filter(token_data=token).first()

        if user:
            project = Project.objects.filter(id=project_id).first()
            if project:
                if project.owner_id == user:
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
        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)
            if user.authority == 1:

                post_body = json.loads(request.body)
                name = post_body.get('name')
                workers_list = post_body.get('workers')
                budget = post_body.get('budget')

                project = Project.objects.create(name=name, budget=budget, is_archived=False, owner_id=user)
                id_project = project.id

                for worker in workers_list:
                    current_user = AppUser.objects.get(id=worker['userId'])

                    role_id = worker['role_id']
                    role = Role.objects.get(id=role_id)

                    data_to_create_employee = {
                        'user_id': current_user,
                        'project_id': project,
                        'rate': worker['rate'],
                        'advance': worker['advance'],
                        'role_id': role
                    }
                    if ProjectEmployee.objects.filter(user_id=current_user, role_id=role, project_id=project):
                        return JsonResponse(EMPLOYEE_IS_EXIST, status=404)

                    else:
                        ProjectEmployee.objects.create(**data_to_create_employee)

                employees = ProjectEmployee.objects.filter(project_id=project)

                serialized_data = serialize('python', employees)

                instance_output_list_of_dicts = []
                for worker in serialized_data:
                    id = worker['pk']
                    current_user = ProjectEmployee.objects.get(id=id).user_id

                    avatar = None if not current_user.avatar else SERV_NAME + str(current_user.avatar.url)

                    fields_dict = worker['fields']
                    instance_output_list_of_dicts.append({'id': id,
                                                          'user_id': current_user.id,
                                                          'rate': fields_dict['rate'],
                                                          'advance': fields_dict['advance'],
                                                          'role_id': fields_dict['role_id'],
                                                          'salary': 0,
                                                          'work_time': 0,
                                                          'avatar': avatar,
                                                          'name': current_user.name,
                                                          'project_id': id_project,
                                                          })

                data = {
                    'id': project.id,
                    'name': project.name,
                    'workers': instance_output_list_of_dicts,
                    'budget': project.budget,
                    'isArchived': project.is_archived,
                    'workTime': project.work_time,
                    'averageRate': project.average_rate,
                }

                return JsonResponse(data, status=201)

            else:
                return JsonResponse(USER_NOT_A_SUB_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdvanceView(View):
    def put(self, request):
        put_body = json.loads(request.body)

        id_worker = put_body.get('workerId')
        advance = put_body.get('advance')

        token = get_token(request)
        user = AppUser.objects.filter(token_data=token).first()

        if user:
            worker = ProjectEmployee.objects.filter(id=id_worker).first()

            if worker:
                if worker.project_id.owner_id == user:
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

        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)

            project = Project.objects.get(id=project_id)

            owner_project = project.owner_id

            role_accounting = Role.objects.get(name='Журнал учета', author_id=owner_project)

            if owner_project == user or ProjectEmployee.objects.filter(project_id=project, user_id=user,
                                                                       role_id=role_accounting):
                post_body = json.loads(request.body)

                date = post_body.get('date')
                work_time = post_body.get('workTime')
                worker_id = post_body.get('worker_id')

                if ProjectEmployee.objects.filter(id=worker_id):

                    current_employee = ProjectEmployee.objects.get(id=worker_id)

                    time_entry = TimeEntry.objects.create(date=date, work_time=work_time, employee_id=current_employee,
                                                          initiator=user)

                    current_user = current_employee.user_id

                    avatar = None if not current_user.avatar else SERV_NAME + str(current_user.avatar.url)

                    data = {
                        'id': time_entry.id,
                        'userId': current_user.name,
                        'rate': current_employee.rate,
                        'advance': current_employee.advance,
                        'role_id': current_employee.role_id.id,
                        'salary': current_employee.salary,
                        'work_time': time_entry.work_time,
                        'avatar': avatar,
                        'name': current_user.name,
                        'project_id': current_employee.project_id.id
                    }

                    return JsonResponse(data, status=200)

                else:

                    return JsonResponse(WORKER_NOT_FOUND, status=404)
            return JsonResponse(NO_PERMISSION_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class WorkerViewWithIndexInEnd(View):
    def delete(self, request, worker_id):
        token = get_token(request)

        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)
            project = Project.objects.filter(owner_id=user)

            worker = ProjectEmployee.objects.get(id=worker_id)

            project_with_need_worker = None
            for i in project:
                if worker.project_id == i:
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

        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)
            worker = ProjectEmployee.objects.get(id=worker_id)

            project = worker.project_id

            if project.owner_id == user:
                post_body = json.loads(request.body)

                role_id = post_body.get('role_id')
                rate = post_body.get('rate')

                if role_id is not None:
                    if Role.objects.filter(id=role_id):
                        role = Role.objects.get(id=role_id)
                        worker.role_id = role
                        worker.save(update_fields=['role_id'])

                    else:
                        return JsonResponse(ROLE_NOT_FOUND_DATA, status=404)

                if rate is not None:
                    worker.rate = rate
                    worker.save(update_fields=['rate'])

                time_emp_on_prj = TimeEntry.objects.filter(employee_id=worker).aggregate(Sum('work_time')),

                work_time = 0 if time_emp_on_prj[0]['work_time__sum'] is None else time_emp_on_prj[0]['work_time__sum']

                data = {
                    'id': worker.id,
                    'userId': worker.user_id.id,
                    'rate': worker.rate,
                    'advance': worker.advance,
                    'role_id': worker.role_id.id,
                    'salary': worker.salary,
                    'work_time': work_time,
                    'name': worker.user_id.name,
                    'project_id': worker.project_id.id,
                }
                return JsonResponse(data, status=200)

            else:
                return JsonResponse(NO_PERMISSION_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AddWorkerView(View):
    def post(self, request, project_id):
        token = get_token(request)

        if AppUser.objects.filter(token_data=token):
            user = AppUser.objects.get(token_data=token)
            if Project.objects.filter(id=project_id):
                project = Project.objects.get(id=project_id)

                if project.owner_id == user:
                    post_body = json.loads(request.body)

                    user_id = post_body.get('userId')
                    need_user = AppUser.objects.get(id=user_id)
                    rate = post_body.get('rate')
                    advance = post_body.get('advance')
                    role_id = post_body.get('role_id')
                    need_role = Role.objects.get(id=role_id)

                    data_to_create = {
                        'user_id': need_user,
                        'rate': rate,
                        'project_id': project,
                        'advance': advance,
                        'role_id': need_role

                    }
                    if ProjectEmployee.objects.filter(user_id=need_user, role_id=need_role, project_id=project):
                        return JsonResponse(EMPLOYEE_IS_EXIST, status=404)

                    else:
                        employee = ProjectEmployee.objects.create(**data_to_create)

                    avatar = None if not employee.user_id.avatar else SERV_NAME + str(employee.user_id.avatar.url)
                    response_data = {
                        'id': employee.id,
                        'userId': employee.user_id.id,
                        'rate': employee.rate,
                        'advance': employee.advance,
                        'role_id': employee.role_id.id,
                        'salary': employee.salary,
                        'work_time': 0,
                        'avatar': avatar,
                        'name': employee.user_id.name,
                        'project_id': employee.project_id.id,
                    }
                    return JsonResponse(response_data, status=200)

                else:
                    return JsonResponse(NO_PERMISSION_DATA, status=404)

            else:
                return JsonResponse(PROJECT_NOT_FOUND_DATA, status=404)

        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=404)
