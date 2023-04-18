from user.models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call the view function and get the response
        response = self.get_response(request)

        # Log user logins
        if request.user.is_authenticated and not request.session.get('logged_in', False):
            UserActivity.objects.create(user=request.user, activity_type='login')
            request.session['logged_in'] = True

        # Log page views
        if request.user.is_authenticated and request.method == 'GET':
            UserActivity.objects.create(user=request.user, activity_type='page_view')

        return response