from django.db import models, IntegrityError

class ExperienceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __unicode__(self):
        return "ExperienceCategory: %s" % (self.name)
    
    def save(self, **kwargs):
        self.name = self.name.lower()
        return super(ExperienceCategory,self).save(**kwargs)
