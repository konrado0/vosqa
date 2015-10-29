from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email

class EmailAuthBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL. using email as username
    """

    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        try:
            validate_email(username)            
            user = UserModel.objects.get(email__iexact=username)
            return super(EmailAuthBackend, self).authenticate(user.username, password)                
        except:
            pass
        UserModel().set_password(password)        
