from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.decorators import login_required

class NoCacheMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Add cache control headers to prevent caching
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response