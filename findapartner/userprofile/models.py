from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.db.models import Q, F

from social_auth.models import UserSocialAuth

from experience_categories.models import ExperienceCategory

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    user_slug = models.SlugField()

    # Other fields here
    extra_info = models.CharField(max_length=500, blank=True, null=True)
    looking_for_position = models.BooleanField(default=True)
    skills = models.ManyToManyField(ExperienceCategory, blank=True, null=True)
    
    def save(self, force_insert=False, force_update=False, using=None):
        self.user_slug = slugify(self.user.username)
        
        slug_version = 1
        while (UserProfile.objects.filter(~Q(user=self.user), user_slug__iexact=self.user_slug).exists()):
            self.user_slug = "%s%s" % (slugify(self.user.username), str(slug_version))
            slug_version += 1
        return super(UserProfile, self).save(force_insert,force_update, using)
    
    def __unicode__(self):
        return "%s" % self.user.username

	def get_absolute_url(self):
		return reverse("user_profile", kwargs={"slug":self.user_slug})
        
    def get_default_avatar(self):
        if self.social_profile and self.social_profile != []:
            for social_profile in self.social_profile:
                if social_profile.provider == "facebook":
                    return "https://graph.facebook.com/%s/picture/" % social_profile.uid
                elif social_profile.provider == "twitter":
                    if social_profile.extra_data and "profile_image_url" in social_profile.extra_data:
                        return social_profile.extra_data["profile_image_url"]
                elif social_profile.provider == "linkedin":
                    if social_profile.extra_data and "picture_url" in social_profile.extra_data:
                        return social_profile.extra_data['picture_url']
        else:
            return None
        
    @property
    def social_profile(self):
        if not hasattr(self,"_social_profile"):
            try:
                self._social_profile = [UserSocialAuth.objects.get(user=self.user)]
            except UserSocialAuth.DoesNotExist:
                self._social_profile = [] 
            except UserSocialAuth.MultipleObjectsReturned:
                self._social_profile = UserSocialAuth.objects.filter(user=self.user).all()
        return self._social_profile
    
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def create_user_social_profile(sender, instance, **kwargs):
    social_profile_type = instance.provider
    social_profile = instance.extra_data
    user_profile = instance.user.get_profile()
    
    if social_profile_type == "linkedin" and instance.extra_data:
        if "skills" in instance.extra_data:
            skills = instance.extra_data["skills"]
            for linkedin_skill in skills['skill']:
                try:
                    pairup_skill = ExperienceCategory.objects.get(name__iexact=linkedin_skill['skill']['name'])
                except ExperienceCategory.DoesNotExist:
                    pairup_skill = ExperienceCategory(name=linkedin_skill['skill']['name'])
                    pairup_skill.save()
                except ExperienceCategory.MultipleObjectsReturned:
                    pairup_skill = ExperienceCategory.objects.filter(name__iexact=linkedin_skill['skill']['name']).all()[0]
                    
                user_profile.skills.add(pairup_skill)
        if "summary" in instance.extra_data and not user_profile.extra_info:
            user_profile.extra_info = instance.extra_data["summary"]
                

post_save.connect(create_user_profile, sender=User, dispatch_uid="findapartner.models")
post_save.connect(create_user_social_profile, sender=UserSocialAuth)


