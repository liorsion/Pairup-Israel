from django.db import models

from userprofile.models import UserProfile

class StatModel(models.Model):
    STAT_TYPES = (
               ('mail', 'mail was sent'),
               ('view', 'user public profile viewed'),
               ('msg', 'user was sent a message')
               )
    stat_type = models.CharField(max_length=4,choices=STAT_TYPES, unique=True, db_index=True)
    stat_counter = models.PositiveIntegerField(default=0)
    stat_updated = models.DateTimeField(auto_now_add=True)
    
    def inc_counter(self, counter_id):
        UserProfile.objects.filter(pk=counter_id).update(stat_counter=F("stat_counter")+1)
        
class UserStatModel(models.Model):
    STAT_TYPES = (
               ('view', 'user public profile viewed'),
               ('msg', 'user was sent a message')
               )
    
    stat_type = models.CharField(max_length=4,choices=STAT_TYPES)
    stat_updated = models.DateTimeField(auto_now_add=True)
    related_user = models.ForeignKey(UserProfile)
    
