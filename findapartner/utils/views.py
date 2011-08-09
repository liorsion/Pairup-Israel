from django.views.generic import View
from django.utils import simplejson
from django.http import HttpResponse

class AjaxView(View):
    
    def dispatch(self, request, *args, **kwargs):
        array_response = super(AjaxView, self).dispatch(request, *args, **kwargs)
        if isinstance(array_response, dict):
            return HttpResponse(simplejson.dumps(array_response), mimetype='application/json')
        else:
            return array_response
    

        