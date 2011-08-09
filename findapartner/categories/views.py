from django.http import HttpResponse
from django.views.generic import View

from findapartner.categories.models import Category

class CategoriesView(View):
    
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', None)
        output_s = ''
        if q:
            existing_cats = Category.objects.filter(name__iexact=q)
            
            if existing_cats:
                for existing_cat in existing_cat:
                    output_s += "%s\n" % existing_cat
                    
        return HttpResponse(output_s)