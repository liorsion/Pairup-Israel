from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User)