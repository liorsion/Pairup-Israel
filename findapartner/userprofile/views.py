from smtplib import SMTPException
from urllib2 import URLError
import urlparse
from django.utils import simplejson

from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login as login_fnc, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q, Count, F
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from registration.views import register
import facebook
from twitter import twitter
from social_auth.models import UserSocialAuth

from findapartner.userprofile.forms import ProfileForm, ContactUserForm, RegistrationFormExpandedUsername
from findapartner.userprofile.models import UserProfile
from findapartner.utils.views import AjaxView
from findapartner.utils.helpers import rand1
from findapartner.partner.models import Partner
from findapartner.stats.models import StatModel, UserStatModel

class SendMessageView(AjaxView):
    
    def post(self, request, *args, **kwargs):
        response = {"success":False, "message": _("Error sending message")}
        
        send_to = kwargs.get("slug", None)
        send_from_name = request.POST.get("from",None)
        send_from_email = request.POST.get("email", None)
        send_message = request.POST.get("message", None)
        
        if not send_from_name:
            response["message"] = _("You must enter your name")
            return response
        if not send_from_email:
            response["message"] = _("You must enter your email")
            return response
        if not send_message:
            response["message"] = _("You must enter a message")
            return response
        
        try:
            send_to_user = UserProfile.objects.get(user_slug__iexact=send_to).user
        except UserProfile.DoesNotExist:
            response["message"] = "%s %s" % (_("Couldn't find user"), send_to)
            return response
        
        try:
            plaintext = get_template('email/new_message.txt')
            htmly     = get_template('email/new_message.html')
            
        # send alerts to followes
            d = Context({'from_name': send_from_name,
                         'from_email': send_from_email,
                         'to_user': send_to_user, 
                         'message': send_message,
                         "sender_profile_link":None
                        })
            
            if request.user.is_authenticated():
                d["sender_profile_link"]="http://pairup.org.il%s" % reverse("user_profile",kwargs={"slug":request.user.get_profile().user_slug})
        
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            
            subject = _('Message from Pairup Israel') 

            msg = EmailMultiAlternatives(subject, text_content, send_from_email, [send_to_user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            
            new_stat, created = StatModel.objects.get_or_create(stat_type='mail')
            StatModel.objects.filter(pk=new_stat.id).update(stat_counter=F('stat_counter')+1)
            msg_sent_stat = UserStatModel(stat_type = "msg",
                                          related_user = send_to_user.get_profile())
            msg_sent_stat.save()
                
        except SMTPException:
            response["message"] = _("Failed sending email message")
            return response
        
        response["message"] = _("Message sent successfully")
        response["success"] = True
        return response
        

class UserSearchView(ListView):
    
    def get_queryset(self):
        search_categories = self.request.POST.get("search_categories", None)
        qs_filter = {"userprofile__looking_for_position":True}
        args = () 
        if search_categories:
            if search_categories.find(",") == -1:
                qs_filter.update({"userprofile__skills__name":search_categories.strip()})
            else:
                search_categories_list = [x.strip() for x in search_categories.split(",")]
                q_value = Q()
                for search_category in search_categories_list:
                    q_value = q_value | Q(userprofile__skills__name=search_category)
                args = (q_value,)
        queryset=User.objects.filter(*args,**qs_filter).annotate(num_hits=Count('id')).order_by('num_hits', '-id')
        return queryset 
      
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class UserSearchViewFeed(Feed):
	title = "Pairup Israel Latest Users To Join"
	link = "/looking/"
	description = "Latest users who joined Pairup Israel looking for new ventures"
	feed_type = Rss201rev2Feed 
	
	def items(self):
		return UserProfile.objects.filter(looking_for_position=True).order_by('-id')[:10]

	def item_title(self, item):
		return item.user.username

	def item_description(self, item):
		return ",".join([skill.name for skill in list(item.skills.all())])
		
	def item_link(self, item):
		return reverse("user_profile", kwargs={"slug":item.user_slug})
		
class UpdateProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    
    def get_object(self, queryset=None):
        self.success_url = reverse("user_profile",kwargs={"slug":self.request.user.get_profile().user_slug})
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        context["active_social_profiles"]=[x.provider for x in UserSocialAuth.objects.filter(user=self.request.user).all()]
        context["existing_partners"] = Partner.objects.filter(archived=False, suggested_by=self.request.user)
        return context
    
class PublicProfile(DetailView):
    model=UserProfile
    slug_field='user_slug'
    
    def get_context_data(self, **kwargs):
        context = super(PublicProfile, self).get_context_data(**kwargs)
        
        if self.request.user.is_authenticated():
            context["form"] = ContactUserForm(initial={"name":self.request.user.username, "email":self.request.user.email})
        else:
            context["form"] = ContactUserForm()
            
        if not self.request.user.is_authenticated() or self.request.user != self.object: #.user:
            msg_sent_stat = UserStatModel(stat_type = "view",
                                          related_user = self.object)
            msg_sent_stat.save()
            
        context["active_social_profiles"]=[x for x in UserSocialAuth.objects.filter(user=self.object.user).all()]
            
        return context
   
class RegisterProfile(View):
    def get(self, request, *args, **kwargs):
        return register(request, form_class=RegistrationFormExpandedUsername, *args, **kwargs)
     
    def post(self, request, *args, **kwargs):
        cookie = facebook.get_user_from_cookie(request.COOKIES,
                                               settings.FACEBOOK_APP_ID,
                                               settings.FACEBOOK_API_SECRET)
        
        if cookie:
            uid = cookie['uid']
            facebook_api = facebook.GraphAPI(cookie['access_token']);
            try:
                profile = facebook_api.get_object('me')
            
                post_req = request.POST.copy()
                post_req["username"] = profile["name"]
                post_req["email"] = profile["email"]
                password = rand1(8)
                post_req["password1"]=post_req["password2"]=password
                request.POST = post_req
            
            except URLError:
                pass
        else:
                profile = {}
            
        http_response = register(request, form_class=RegistrationFormExpandedUsername, *args, **kwargs) 
        
        if "email" in profile and isinstance(http_response, HttpResponseRedirect):
            try:
                new_user = User.objects.get(email=profile["email"])
                UserSocialAuth.objects.create(user=new_user, 
                                              uid=uid,
                                              provider="facebook",
                                              extra_data=simplejson.dumps({u'access_token': cookie['access_token'], 
                                                                            u'expires': None, 
                                                                            u'id': uid,
                                                                            u'public_profile_url':'https://graph.facebook.com/%s' % (profile["username"])
                                                                          })
                                              )
            except User.DoesNotExist:
                pass
        return http_response
            

class AssociateFacebook(AjaxView):
    def post(self, request, *args, **kwargs):
        response = {"success":False, "message": _("Error associating Facebook accounts")}
        
        cookie = facebook.get_user_from_cookie(request.COOKIES,
                                               settings.FACEBOOK_APP_ID,
                                               settings.FACEBOOK_API_SECRET)
        
        if cookie:
            uid = cookie['uid']
            facebook_api = facebook.GraphAPI(cookie['access_token']);
            
            try:
                user_assoc = UserSocialAuth.objects.get(uid=uid)
                if user_assoc.user==request.user:
                    
                    try:
                        profile = facebook_api.get_object('me')
                        user_assoc.extra_data=simplejson.dumps({u'access_token': cookie['access_token'], 
                                                                                u'expires': None, 
                                                                                u'id': uid,
                                                                                u'public_profile_url':'https://graph.facebook.com/%s' % (profile["username"])
                                                                              })
                        user_assoc.save()
                        response["message"]=_("You're already associated with a Facebook account, data updated")
                    except URLError:
                        response["message"]=_("You're already associated with a Facebook account")
                else:
                    response["message"]=_("Facebook account is already associated with a different user")
            except UserSocialAuth.DoesNotExist: 
                facebook_api = facebook.GraphAPI(cookie['access_token']);
                try:
                    profile = facebook_api.get_object('me')
                    UserSocialAuth.objects.create(user=request.user, 
                                                  uid=uid,
                                                  provider="facebook",
                                                  extra_data=simplejson.dumps({u'access_token': cookie['access_token'], 
                                                                            u'expires': None, 
                                                                            u'id': uid,
                                                                            u'public_profile_url':'https://graph.facebook.com/%s' % (profile["username"])
                                                                          }))
                
                    response.update({"success":True,"message":_("Association was successful")})
                except URLError:
                    response["message"]=_("Error accessing Facebook, please try again shortly")
            
        return response
                
class TwitterRegister(View):
    def get(self, request, *args, **kwargs):
        twitter_cookie = twitter.get_user_from_cookie(request.COOKIES,
                                                      settings.TWITTER_CONSUMER_SECRET)
        if twitter_cookie:
            uid = twitter_cookie['uid']
            post_req = request.POST.copy()
            #post_req["email"] = profile["email"]
            password = rand1(8)
            post_req["password1"]=post_req["password2"]=password
            request.POST = post_req
        else:
            profile = {}
                
        http_response = register(request, form_class=RegistrationFormExpandedUsername, *args, **kwargs) 
        
        if twitter_cookie and isinstance(http_response, HttpResponseRedirect):
            try:
                new_user = User.objects.get(username=profile["username"])
                UserSocialAuth.objects.create(user=new_user, 
                                              uid=uid,
                                              provider="twitter")
            except User.DoesNotExist:
                pass
        return http_response
                
class FacebookLogin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            cookie = facebook.get_user_from_cookie(request.COOKIES,
                                                   settings.FACEBOOK_APP_ID,
                                                   settings.FACEBOOK_API_SECRET)
            
            if cookie:
                uid = cookie['uid']
                facebook_api = facebook.GraphAPI(cookie['access_token']);
                try:
                    profile = facebook_api.get_object('me')
                    
                    user_auth = user = authenticate(name="facebook",facebook=profile,response=profile,uid=uid)
                    if user_auth:
                        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
                        netloc = urlparse.urlparse(redirect_to)[1]
    
                        # Use default setting if redirect_to is empty
                        if not redirect_to:
                            redirect_to = settings.LOGIN_REDIRECT_URL
            
                        # Security check -- don't allow redirection to a different
                        # host.
                        elif netloc and netloc != request.get_host():
                            redirect_to = settings.LOGIN_REDIRECT_URL
            
                        # Okay, security checks complete. Log the user in.
                        login_fnc(request, user)
            
                        if request.session.test_cookie_worked():
                            request.session.delete_test_cookie()
            
                        return HttpResponseRedirect(redirect_to)
                except URLError:
                    pass
            
        return login(request, *args, **kwargs)
        