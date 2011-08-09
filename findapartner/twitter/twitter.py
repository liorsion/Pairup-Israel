#!/usr/bin/env python
#
# Copyright 2011 Lior Sion
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Python client library for the Twitter Platform.

    user = facebook.get_user_from_cookie(self.request.cookies, 
                                         consumer_secret_key)
    if user:
        ...
"""

import cgi
import time
import urllib2 
import urllib
import hashlib
import hmac
import base64
import logging

# Find a JSON parser
try:
    import simplejson as json
except ImportError:
    try:
        from django.utils import simplejson as json
    except ImportError:
        import json
_parse_json = json.loads



def get_user_from_cookie(cookies, app_secret):
    """Parses the cookie set by the official Twitter OAuth request.

    """
    cookie = cookies.get("twitter_anywhere_identity")
    if not cookie: return None
    args = cookie.split(":")
    uid = args[0]
    
    expected_sig = hashlib.sha1("%s%s" % (uid,app_secret)).hexdigest()
    
    if expected_sig == args[1]:
        return {'uid':uid}
    else:
        return None

