# adminpanel/context_processors.py
from adminpanel.models import User

def session_user(request):
    user = None
    user_dict = request.session.get("user")
    if user_dict and user_dict.get("logged_in"):
        try:
            user = User.objects.get(id=user_dict["id"])
        except User.DoesNotExist:
            user = None
    return {'request_user': user}
