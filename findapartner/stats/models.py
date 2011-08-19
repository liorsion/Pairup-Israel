from django.db import models

class StatModel(models.Model):
    STAT_TYPES = (
               ('mail', 'mail was sent'),
               )
    stat_type = models.CharField(max_length=4,choices=STAT_TYPES, unique=True, db_index=True)
    stat_counter = models.PositiveIntegerField(default=0)