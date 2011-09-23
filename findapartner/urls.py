from django.conf.urls.defaults import patterns, include, url

from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

from findapartner.partner.views import PairupView, PartnerActionView, ListPartnersView, ListPartnerViewFeed, PublicPartnerView
from findapartner.partner.models import Partner 
from findapartner.experience_categories.views import ExperienceCategoriesView
from findapartner.categories.views import CategoriesView
from findapartner.userprofile.views import UpdateProfileView, PublicProfile, SendMessageView, RegisterProfile, FacebookLogin, AssociateFacebook, TwitterRegister, UserSearchView, UserSearchViewFeed
from findapartner.views import IndexView

urlpatterns = patterns('',
                       
    url(r'^accounts/register/twitter/$',TwitterRegister.as_view(),name='twitter_reg'),
    url(r'^accounts/register/$',RegisterProfile.as_view(),name='registration_register'),
    url(r'^accounts/login/facebook/$',FacebookLogin.as_view(),name='facebook_login'),
    url(r'^accounts/login-error/$', direct_to_template, {'template':'auth/login-error.html'}, name='error'),
    (r'^accounts/', include('registration.urls')),
    url(r'^profile/associate/$', login_required(AssociateFacebook.as_view()), name="associate_profile_facebook"),
    url(r'^profile/edit/$', login_required(UpdateProfileView.as_view()), name="edit_profile"),
    url(r'accounts/social/', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^robots\.txt$', direct_to_template,{'template': 'robots.txt', 'mimetype': 'text/plain'}),
    
    url(r'^experience_categories/get_experience_categories/$', ExperienceCategoriesView.as_view(), name="get_experience_categories"),
    url(r'^ideas/get_idea_categories/$', CategoriesView.as_view(), name="get_categories"),
    
    
    url(r'^users/(?P<slug>[\w\-\"]+)/message/$',SendMessageView.as_view(),name="send_message"),
    url(r'^users/(?P<slug>[\w\-\"]+)/$',PublicProfile.as_view(),name="user_profile"),
    url(r'^partner_request/(?P<action>[\w\-\"]+)/$',login_required(PartnerActionView.as_view()), name="update_event_action"),
    url(r'^open_positions/(?P<pk>\d+)/$',PublicPartnerView.as_view(),name="public_partner"),
    url(r'^looking/$',UserSearchView.as_view(),name="look_for_partner"),
	url(r'^looking/feed/$',UserSearchViewFeed(),name="look_for_partner_feed"),
    url(r'^add_partner_position/$',login_required(PairupView.as_view()),name="add_position"),
    url(r'^list/$',ListPartnersView.as_view(model=Partner),name="list_positions"),
    url(r'^list/feed/$',ListPartnerViewFeed(),name="list_positions_feed"),
    url(r'^added/$',direct_to_template, {'template': 'partner/partner_added.html'}, name="position_added"),
    (r'^sentry/', include('sentry.web.urls')),
    url(r'^about/$',direct_to_template, {'template': 'about.html'}, name="about"),
    (r'^$', IndexView.as_view())
)
