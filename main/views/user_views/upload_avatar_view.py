from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.const_data.serv_info import SERV_NAME
from main.const_data.template_errors import NO_FILE_DATA, USER_NOT_FOUND_DATA
from main.parsers import get_token
from main.services.user.selectors import get_app_user_by_token


@method_decorator(csrf_exempt, name='dispatch')
class UploadAvatar(View):
    def post(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            files = request.FILES
            if 'file' in files:
                avatar = files['file']

                need_user.avatar = avatar
                need_user.save(update_fields=['avatar'])
                output_data = {
                    'path': str(need_user.avatar.url),
                    'baseURL': SERV_NAME
                }
                return JsonResponse(output_data, status=200)
            else:
                return JsonResponse(NO_FILE_DATA, status=404)
        else:
            return JsonResponse(USER_NOT_FOUND_DATA, status=401)
