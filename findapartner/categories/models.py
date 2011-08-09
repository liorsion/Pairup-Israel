from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return "Category: %s" % (self.name)
    