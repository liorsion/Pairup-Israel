from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext as _

from experience_categories.models import ExperienceCategory
from findapartner.utils.forms import CategoryTagModelMultipleChoiceField
from registration.forms import RegistrationFormUniqueEmail

from findapartner.userprofile.models import UserProfile

class ProfileForm(ModelForm):
    
    extra_info = forms.CharField(required=False, widget=forms.Textarea)
    looking_for_position = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    skills = CategoryTagModelMultipleChoiceField(queryset=ExperienceCategory.objects.all(),
                                                label="Experience Categories",
                                                to_field_name='name',
                                                required=False,
                                                widget=forms.TextInput(attrs={'name':'tags', 'id':'tags'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'looking_for_position', 'extra_info','skills')
        
    def __init__(self, *args,  **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if "instance" in kwargs and kwargs["instance"]:
            user_profile = kwargs["instance"].get_profile()
            self.initial["extra_info"] = user_profile.extra_info
            self.initial["looking_for_position"] = user_profile.looking_for_position
            if user_profile.skills is not None:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                self.initial["skills"] = ", ".join([skill.name for skill in user_profile.skills.all()])
                
    def save(self, commit=True):
        new_instance = super(ProfileForm,self).save(commit)
        if new_instance:
            profile = new_instance.get_profile()
            if "extra_info" in self.cleaned_data:
                profile.extra_info = self.cleaned_data["extra_info"]
            if "looking_for_position" in self.cleaned_data:
                profile.looking_for_position = self.cleaned_data["looking_for_position"]
            if "skills" in self.cleaned_data:
                profile.skills = self.cleaned_data["skills"]
            profile.save()
        return new_instance
    
class ContactUserForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True,
                              widget=forms.Textarea())
    
    def __init__(self, **kwargs):
        super(ContactUserForm, self).__init__(**kwargs)
        if 'initial' in kwargs:
            self.fields["email"].widget = forms.HiddenInput()
            self.fields["name"].widget = forms.HiddenInput()
        
    
class RegistrationFormExpandedUsername(RegistrationFormUniqueEmail):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs={"required":True}),
                                label=_(u'username'))