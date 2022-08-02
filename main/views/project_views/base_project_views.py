from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from main.const_data.template_errors import *

from main.parsers import *
from main.serializers.project_serializers.create_serializers import ProjectSerializerForCreate
from main.serializers.project_serializers.project_serializers import ProjectSetCompleteSerializer, ProjectSerializerLong
from main.services.project.selectors import get_projects_by_owner, get_all_project
from main.services.user.selectors import get_app_user_by_token


class SetCompleteProjectView(UpdateAPIView):
    serializer_class = ProjectSetCompleteSerializer

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            self.queryset = get_projects_by_owner(owner_project=user)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(SUCCESS_DATA, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class ProjectCreateAPIView(CreateAPIView):
    serializer_class = ProjectSerializerForCreate
    queryset = get_all_project()

    def create(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            project = serializer.save(owner=user)
            return Response(ProjectSerializerLong(project).data, status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

# @method_decorator(csrf_exempt, name='dispatch')
# class ProjectCreateAPIView(View):
#     def post(self, request):
#         token = get_token(request)
#         user = get_app_user_by_token(token=token)
#         if user:
#             if user.authority == 1:
#                 post_body = json.loads(request.body)
#                 name = post_body.get('name')
#                 roles_list = post_body.get('roles')
#                 workers_list = post_body.get('workers')
#                 budget = post_body.get('budget')
#                 currency = post_body.get('currency')
#                 project = Project.objects.create(name=name, budget=budget, is_archived=False, owner=user,
#                                                  currency=currency)
#
#                 roles = []
#                 for role_from_body in roles_list:
#                     del role_from_body['id']
#                     role_from_body['project'] = project
#                     role_from_body['is_base'] = False
#                     role_from_body['author'] = user
#                     roles.append(Role.objects.create(**role_from_body))
#
#                 for worker in workers_list:
#                     current_user = get_app_user_by_id(id=worker['userId'])
#                     role = get_role_by_name_and_author_and_project(name=worker['roleName'], author=user,
#                                                                    project=project)
#                     data_to_create_employee = {
#                         'user': current_user,
#                         'project': project,
#                         'advance': worker['advance'],
#                         'role': role
#                     }
#                     ProjectEmployee.objects.create(**data_to_create_employee)
#
#                 workers_output_list_of_dicts = get_pretty_view_workers_by_project(project=project)
#
#                 roles_output_list_of_dicts = get_pretty_view_roles_by_project(project=project)
#
#                 output_data = get_full_output_project_data(project=project, workers=workers_output_list_of_dicts,
#                                                            roles=roles_output_list_of_dicts)
#
#                 return JsonResponse(output_data, status=201)
#
#             else:
#                 return JsonResponse(USER_NOT_A_SUB_DATA, status=404)
#
#         else:
#             return JsonResponse(USER_NOT_FOUND_DATA, status=404)
