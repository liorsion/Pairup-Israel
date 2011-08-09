from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from categories.models import Category
from experience_categories.models import ExperienceCategory

class Partner(models.Model):
    general_description = models.CharField(max_length=500)
    idea = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    experience_general = models.CharField(max_length=500, blank=True, null=True)
    experience_categories = models.ManyToManyField(ExperienceCategory, blank=True, null=True)
    add_date = models.DateField(auto_now_add=True)
    last_update = models.DateField(auto_now=True)
    suggested_by = models.ForeignKey(User)
    archived = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "Looking for a cofounder: %s" % self.idea
    
    def get_absolute_url(self):
        return reverse("public_partner", kwargs={"pk":self.pk})