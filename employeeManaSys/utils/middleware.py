from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class Auth(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == '/login/':
            return
        user = request.session.get('user')
        if user:
            return
        return redirect('/login/')