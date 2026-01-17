from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.decorators import login_required

class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent browser caching of authenticated pages.
    This ensures that logged-out users cannot access cached pages
    by using the browser's back button.
    """
    def process_response(self, request, response):
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Add cache control headers to prevent caching
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response