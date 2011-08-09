from  django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

from findapartner.partner.forms import PairupForm
from findapartner.partner.models import Partner
from findapartner.utils.views import AjaxView

class PublicPartnerView(DetailView):
    model=Partner
            
class ListPartnersView(ListView):
    
    def get_queryset(self):
        exp_cat = self.request.GET.get("exp_cat", None)
        qs_filter = {"archived":False} 
        if exp_cat:
            qs_filter.update({"experience_categories__name":exp_cat})
        queryset=Partner.objects.filter(**qs_filter)
        return queryset 
        
    
class PairupView(CreateView):
    form_class = PairupForm
    template_name = "partner/add_partner.html"
    model = Partner
    
    def get_context_data(self, **kwargs):
        context = super(PairupView, self).get_context_data(**kwargs)
        context["form"].fields["categories"].label = "Idea Categories"
        context["form"].fields["experience_categories"].label = "Experience Needed"
        
        context["existing_partners"] = Partner.objects.filter(archived=False, suggested_by=self.request.user)
        return context
    
    def get_success_url(self):
        return reverse("position_added")
    
    def get_initial(self):
        return {"suggested_by":self.request.user}
    
    def get_form_kwargs(self):
        kwargs = super(PairupView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
class PartnerActionView(AjaxView):
    def post(self, request, *args, **kwargs):
        response = {"success":False, "message": _("Error updating partner request")}
        
        partner_id = request.POST.get("ad_id", None)
        
        if partner_id:
            try:
                partner_ad = Partner.objects.get(pk=partner_id)
                if partner_ad.suggested_by == request.user:
                    action = kwargs.get("action", None)
                    if action:
                        try:
                            method = getattr(self, action)
                            response.update(method(partner_ad))
                        except AttributeError:
                            response.update({"message":_("Method not allowed")})
                    else:
                        response.update({"message":_("Action not found")})
                else:
                    response.update({"message":_("You are not allowed to update this ad")})
            except Partner.DoesNotExist:
                response.update({"message":_("Partner request not found")})
        else:
            response.update({"message":_("Partner request id not found")})
        return response
    
    def update(self, partner_ad):
        partner_ad.save()
        return {"success":True,"message":_("Ad updated")}
        
    def delete(self, partner_ad):
        partner_ad.archived = True
        partner_ad.save()
        return {"success":True,"message":_("Ad deleted")}
