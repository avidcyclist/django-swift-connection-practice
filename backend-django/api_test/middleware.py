from django.shortcuts import redirect

class PasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if the user has a profile and if they need to change their password
            if hasattr(request.user, 'profile') and not request.user.profile.password_changed:
                if request.path != '/password-change/':  # Avoid redirect loop
                    return redirect('/password-change/')
        return self.get_response(request)