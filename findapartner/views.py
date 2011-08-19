from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from findapartner.partner.models import Partner
from findapartner.stats.models import StatModel

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context["total_users"] = User.objects.all().count()
        context["total_open_positions"] = Partner.objects.all().count()
        context["intro_count"] = StatModel.objects.get_or_create(stat_type='mail')[0].stat_counter
        return context