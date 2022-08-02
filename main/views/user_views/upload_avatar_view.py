from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.parsers import get_token
from main.serializers.user_serializers.user_avatar_serializers import FileSerializer
from main.services.user.selectors import get_app_user_by_token, get_all_files


class UploadFile(CreateAPIView):
    serializer_class = FileSerializer
    queryset = get_all_files()

    def create(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            request.data['user'] = user.id
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

# @method_decorator(csrf_exempt, name='dispatch')
# class UploadFile(View):
#     def post(self, request):
#         token = get_token(request)
#         need_user = get_app_user_by_token(token=token)
#         if need_user:
#             files = request.FILES
#             if 'file' in files:
#                 avatar = files['file']
#
#                 need_user.avatar = avatar
#                 need_user.save(update_fields=['avatar'])
#                 output_data = {
#                     'path': str(need_user.avatar.url),
#                     'baseURL': SERV_NAME
#                 }
#                 return JsonResponse(output_data, status=200)
#             else:
#                 return JsonResponse(NO_FILE_DATA, status=400)
#         else:
#             return JsonResponse(USER_NOT_FOUND_DATA, status=401)
