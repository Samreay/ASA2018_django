from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings

from asa18.models import Presentation

from lxml import html

class Command(BaseCommand):
    help = 'Send an email to all participants with rejected talks, offering ' \
           'them the option of converting to a poster or withdrawing'

    email_body = "Dear %s,\n\n" \
                 "Thank you for your abstract submission for a " \
                 "talk at %s.\n\n" \
                 "Regrettably, we must inform you that your abstract '%s' " \
                 "has not been accepted for a talk.\n\n" \
                 "However, we have accepted it as a poster instead, and " \
                 "would encourage you to present it as a poster. To do so, " \
                 "please click/visit this URL: " \
                 "%s \n" \
                 "If you simply wish to withdraw your talk abstract, please " \
                 "click/visit this URL: %s \n\n" \
                 "If you wish to present your work as a poster, and your " \
                 "abstract requires alterations, we are happy to assist you. " \
                 "Please contact %s. We have " \
                 "included your talk title and abstract below for your " \
                 "reference.\n\n" \
                 "Regards,\n%s LOC\n\n" \
                 "--------\n" \
                 "%s\n" \
                 "%s"

    def handle(self, *args, **options):
        # Get all the presentations that:
        # - Are talks
        # - Are currently flagged as rejected
        rejected_talks = Presentation.objects.filter(
            status='r',
            type='t',
        )

        # Generate the list of mail tuples
        mail_tuples = [
            ('ASA 2018 - Talk not accepted - option to convert to poster',
             self.email_body % (
                 t.presenter.given_names,
                 'ASA 2018',
                 t.title,
                 'http://%s%s'
                 '?action=convert-to-poster&key=%s' % (
                     settings.ALLOWED_HOSTS[0],
                     t.get_mgmt_url(), t.generate_secret_key(),
                 ),
                 'http:/%s%s'
                 '?action=withdraw-rejected&key=%s' % (
                     settings.ALLOWED_HOSTS[0],
                     t.get_mgmt_url(), t.generate_secret_key(),
                 ),
                 settings.REGISTRATION_EMAIL,
                 settings.GLOBAL_PAGE_TITLE,
                 t.title,
                 html.fromstring(t.abstract).text_content(),
             ).replace('http://web/', 'http://asa2018.swin.edu.au/'),
             settings.REGISTRATION_EMAIL,
             [t.presenter.email, ])
            for t in rejected_talks
        ]

        # Send the email
        if len(mail_tuples) > 0:
            print('Sending rejected mail to %d talk presenters' %
                  len(mail_tuples))
            send_mass_mail(mail_tuples, fail_silently=False)
        else:
            print('No rejected talks - no emails sent')
