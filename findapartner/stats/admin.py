from django.contrib import admin

from findapartner.stats.models import StatModel, UserStatModel
admin.site.register(StatModel)
admin.site.register(UserStatModel)