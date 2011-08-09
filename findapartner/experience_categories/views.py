from django.http import HttpResponse
from django.views.generic import View

from findapartner.experience_categories.models import ExperienceCategory

class ExperienceCategoriesView(View):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        if not q:
            q = request.GET.get('term', None)
        output_s = ''
        if q:
            q = q.lower()
            existing_cats = ExperienceCategory.objects.filter(name__startswith=q)
            
            if existing_cats:
                for existing_cat in existing_cats:
                    output_s += "%s\n" % existing_cat
                    
        return HttpResponse(output_s)