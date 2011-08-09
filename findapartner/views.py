from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from findapartner.partner.models import Partner

class IndexView(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context["total_users"] = User.objects.all().count()
        context["total_open_positions"] = Partner.objects.all().count()
        
        return context