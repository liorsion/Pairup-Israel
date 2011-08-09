from datetime import date, timedelta 
from smtplib import SMTPException

#from celery.schedules import crontab
#from celery.task.base import PeriodicTask

from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives, send_mail

from findapartner.partner.models import Partner

import logging
logger = logging.getLogger("partner.tasks")

#class checkoverduepartner(PeriodicTask):
class checkoverduepartner(object):
    #run_every = crontab(hour=19, minute=30) # run every day at 19:30 am
    
    def run(self, **kwargs):
        #logger = checkoverduepartner.get_logger()
        logger.debug("Ping user mail was called")
    
        last_month = date.today()-timedelta(weeks=1)
        
        overdue_partners = Partner.objects.filter(archived=False,last_update__lt=last_month)
        
        logger.info("Ovredue partner request daily run. (%d) overdue requests found" % overdue_partners.count())
        
        for overdue_partner in overdue_partners:
            overdue_partner.archived = True
            overdue_partner.save()
            
            try:
                plaintext = get_template('email/partner_offer_overdue.txt')
                htmly     = get_template('email/partner_offer_overdue.html')
                
            # send alerts to followes
                d = Context({'partner_link': "http://pairup.org.il%s" % overdue_partner.get_absolute_url(),
                             'to_user': overdue_partner.suggested_by, 
                            })
                
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                
                subject = _('Message from Pairup Israel') 
    
                msg = EmailMultiAlternatives(subject, text_content, "info@pairup.org.il", [overdue_partner.suggested_by.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
                    
            except SMTPException:
                response["message"] = _("Failed sending email message")
                return response
