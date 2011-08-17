from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class CategoryTagModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    case_sensitive = True
    
    def __init__(self, queryset, case_sensitive=True, *args, **kwargs):
        self.case_sensitive = case_sensitive
        super(CategoryTagModelMultipleChoiceField,self).__init__(queryset, *args, **kwargs)
        
    def clean(self, value):
        value = list(set([value.lower() for value in value.split(',')]))
        for val in value:
            if self.case_sensitive:
                kwargs = {"%s__iexact" % (self.to_field_name):val,
                          "defaults":{self.to_field_name: val}}
            else:
                kwargs = {self.to_field_name:val}
            try:
                val, created = self.queryset.get_or_create(**kwargs)
            except MultipleObjectsReturned:
                pass
        return super(CategoryTagModelMultipleChoiceField, self).clean(value) 
