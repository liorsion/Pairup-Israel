from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django import forms

from findapartner.partner.models import Partner
from categories.models import Category
from experience_categories.models import ExperienceCategory
from findapartner.utils.forms import CategoryTagModelMultipleChoiceField

class PairupForm(ModelForm):

    general_description = forms.CharField(label="What are you looking for?",
                                          widget=forms.Textarea)
    idea = forms.CharField(label="Describe the idea / venture",
                           widget=forms.Textarea)
    categories = CategoryTagModelMultipleChoiceField(queryset=Category.objects.all(),
                                                     label="Venture categories",
                                                     to_field_name="name",
                                                     required=False, 
                                                     case_sensitive = False,
                                                     widget=forms.TextInput(attrs={'name':'category_tags', 'id':'category_tags'}))
    experience_general = forms.CharField(label="General description of experience",
                                         required=False,
                                         widget=forms.Textarea)
    experience_categories = CategoryTagModelMultipleChoiceField(queryset=ExperienceCategory.objects.all(),
                                                                label="Experience Categories",
                                                                to_field_name='name',
                                                                required=False,
                                                                case_sensitive = False,
                                                                widget=forms.TextInput(attrs={'name':'tags', 'id':'tags'}))
    suggested_by = forms.ModelChoiceField(queryset=User.objects.all(),widget=forms.HiddenInput())
    
    class Meta:
        model = Partner
        exclude = ('archived',)
        fields = ('general_description', 'idea', 'categories', 'city', 'experience_general', 'experience_categories', 'suggested_by',)
        
    def __init__(self, *args, **kwargs): 
        self.suggested_by = kwargs.pop("user", None) 
        super(PairupForm, self).__init__(*args, **kwargs) 
        
