from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import email_re

import logging
logger = logging.getLogger("utils.backend")

class EmailUserBackend(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = True
    supports_inactive_user = True
    
    def authenticate(self, username=None, password=None):
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
            except User.MultipleObjectsReturned:
                logger.error("More than one user exist for address [%s]" % username)
                
        return super(EmailUserBackend,self).authenticate(username, password)
    
class CaseInsensitiveModelBackend(object):
    supports_object_permissions = False
    supports_anonymous_user = False
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None