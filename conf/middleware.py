# middleware.py
from django.shortcuts import redirect

class GlobalLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        match = request.resolver_match

        if match:
            view = match.func

            # 🔓 Allow views marked as public
            if getattr(view, "login_not_required", False) or \
               getattr(getattr(view, "view_class", None), "login_not_required", False):
                return self.get_response(request)

        # 🔒 Default: require login
        if not request.user.is_authenticated:
            return redirect("login")

        return self.get_response(request)