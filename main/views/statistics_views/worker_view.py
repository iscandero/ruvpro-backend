from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class GetWorkerStatistic(View):
    def get(self, request):
        pass
        # token = get_token(request)
        # user = get_app_user_by_token(token=token)
