from django.conf import settings

def social_context(request):
    "Returns facebook context variables."
    context_extras = {"FACEBOOK_APP_ID":settings.FACEBOOK_APP_ID,
                      "FACEBOOK_API_SECRET": settings.FACEBOOK_API_SECRET,
                      "FACEBOOK_EXTENDED_PERMISSIONS": settings.FACEBOOK_EXTENDED_PERMISSIONS,
                      "TWITTER_API_KEY": settings.TWITTER_CONSUMER_KEY}
    return context_extras
