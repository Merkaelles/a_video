import time
from django.utils.deprecation import MiddlewareMixin
from users.models import OperationLog


class OperationLogMiddleware(MiddlewareMixin):
    def __init__(self, *args):
        super().__init__(*args)
        self.start_time = None
        self.flag = False
        self.id = id   # 当前操作的主键

    def process_request(self, request):
        self.start_time = time.time()
        ip = request.META.get('REMOTE_ADDR')
        method = request.method
        path = request.path
        try:
            username = request.user.username
        except Exception as e:
            username = None
        if username:
            ol = OperationLog.objects.create(ip=ip, method=method, path=path, username=username)
            self.flag = True
            self.id = ol.id

    def process_response(self, request, response):
        if not self.flag:
            return response
        response_type = request.headers.get('Content-Type')
        status = response.status_code
        end = time.time()
        duration = round((end - self.start_time) * 1000)
        ol = OperationLog.objects.get(id=self.id)
        ol.status = status
        ol.response_type = response_type
        ol.duration = duration
        if status < 400:
            ol.is_success = True
        ol.save()
        return response




