from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail
from django.utils.timezone import localtime
from django.conf import settings

from asa18.models import Presentation

from lxml import html

class Command(BaseCommand):
    help = 'Send an email to all participants with rejected talks, offering ' \
           'them the option of converting to a poster or withdrawing'

    email_body = "Dear %s,\n\n" \
                 "Thank you for your abstract submission " \
                 "at %s.\n\n" \
                 "We are pleased to inform you that your abstract '%s' has " \
                 "now been accepted for a poster presentation. We will be in " \
                 "touch soon regarding the ID number and positioning of " \
                 "your poster.\n\n " \
                 "Please contact %s if you have any " \
                 "questions or concerns. We have " \
                 "included your poster title and abstract below for your " \
                 "reference.\n\n" \
                 "Regards,\n%s LOC\n\n" \
                 "--------\n" \
                 "%s\n" \
                 "%s"

    def handle(self, *args, **options):
        # Get all the presentations that:
        # - Are talks
        # - Are currently flagged as accepted
        accepted_talks = Presentation.objects.filter(
            status='a',
            type='p',
        )

        # Generate the list of mail tuples
        mail_tuples = [
            ('ASA 2018 - Poster accepted',
             self.email_body % (
                 t.presenter.given_names,
                 'ASA 2018',
                 t.title,
                 settings.REGISTRATION_EMAIL,
                 settings.GLOBAL_PAGE_TITLE,
                 t.title,
                 html.fromstring(t.abstract).text_content(),
             ),
             settings.REGISTRATION_EMAIL,
             [t.presenter.email, ])
            for t in accepted_talks
        ]

        # Send the email
        if len(mail_tuples) > 0:
            print('Sending accepted mail to %d poster presenters' %
                  len(mail_tuples))
            send_mass_mail(mail_tuples, fail_silently=False)
        else:
            print('No matching posters - no emails sent')

