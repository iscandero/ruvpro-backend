import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.template_errors import *
from main.models import *
from main.parsers import *

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):
    def post(self, request):
        token = get_token(request)
        if User.objects.filter(token_data=token):
            user = User.objects.get(token_data=token)
            if user.authority == 1:

                post_body = json.loads(request.body)
                name = post_body.get('name')
                workers_list = post_body.get('workers')
                budget = post_body.get('budget')

                project = Project.objects.create(name=name, budget=budget, is_archived=False, owner_id=user)

                for worker in workers_list:
                    current_user = User.objects.get(id=worker['userId'])

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
                        employee = ProjectEmployee.objects.create(**data_to_create_employee)

                employees = ProjectEmployee.objects.filter(project_id=project)
                serialized_data = serialize('python', employees)
                count_of_instance = employees.count()
                instance_output_list_of_dicts = list(dict())

                for i in range(count_of_instance):
                    id = serialized_data[i]['pk']
                    current_user = ProjectEmployee.objects.get(id=id).user_id
                    avatar = None if not current_user.avatar else str(current_user.avatar.url)
                    fields_dict = serialized_data[i]['fields']
                    instance_output_list_of_dicts.append({'id': id,
                                                          'user_id': current_user.id,
                                                          'rate': fields_dict['rate'],
                                                          'advance': fields_dict['advance'],
                                                          'role_id': fields_dict['role_id'],
                                                          'salary': 0,
                                                          'work_time': 0,
                                                          'avatar': avatar,
                                                          'name': current_user.name,
                                                          'project_id': project.id,
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
class TimeEntryView(View):
    def post(self, request, project_id):
        token = get_token(request)

        if User.objects.filter(token_data=token):
            user = User.objects.get(token_data=token)

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

                    avatar = None if not current_user.avatar else str(current_user.avatar.url)

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

        if User.objects.filter(token_data=token):
            user = User.objects.get(token_data=token)
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

        if User.objects.filter(token_data=token):
            user = User.objects.get(token_data=token)
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

        if User.objects.filter(token_data=token):
            user = User.objects.get(token_data=token)
            if Project.objects.filter(id=project_id):
                project = Project.objects.get(id=project_id)

                if project.owner_id == user:
                    post_body = json.loads(request.body)

                    user_id = post_body.get('userId')
                    need_user = User.objects.get(id=user_id)
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

                    avatar = None if not employee.user_id.avatar else str(employee.user_id.avatar.url)
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


# class ViewPaginatorMixin(object):
#     per_page = 3
#     current_page = 1
#
#     def paginate(self, object_list, page=current_page, limit=per_page, **kwargs):
#         try:
#             page = int(page)
#             if page < self.current_page:
#                 page = self.current_page
#         except (TypeError, ValueError):
#             page = self.current_page
#
#
#         paginator = Paginator(object_list, limit)
#
#         if EmptyPage:
#             objects = paginator.page(paginator.num_pages)
#
#         meta = {
#             'totalCount': objects.has_previous() and objects.previous_page_number() or None,
#             'pageCount': objects.has_next() and objects.next_page_number() or None,
#             'currentPage': list(objects),
#             'perPage':
#         }
#         return meta

# @method_decorator(csrf_exempt, name='dispatch')
# class PaginateProjectView(View):
#     def get(self, request, project_id):
#
