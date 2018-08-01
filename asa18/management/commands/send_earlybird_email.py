from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail
from django.conf import settings
from django.urls import reverse

from asa18.models import Registration, Attendee

class Command(BaseCommand):
    help = 'Send an email to all participants requesting updated dietary ' \
           'restriction information'

    email_body = "Dear %s,\n\n" \
                 "Thank you for your registration to attend ASA 2018.\n\n" \
                 "Our system has detected that your registration has yet to " \
                 "be paid for. Please note that payment is required by " \
                 "11.59pm AEST, Wednesday 24 May to retain your 'early-bird' " \
                 "registration option. Failure to pay by this date " \
                 "will result in your registration being " \
                 "switched from the 'early-bird' option to the relevant " \
                 "full-price option, with the associated cost increase.\n\n" \
                 "Payment can be made using the 'Check Registration' " \
                 "function, available at " \
                 "https://%s.\n\n" \
                 "If you are having issues making payment, or you believe " \
                 "you have already paid, please let us " \
                 "know.\n\n" \
                 "Regards,\n%s LOC"

    def handle(self, *args, **options):
        # Get all the attendees who:
        # - Have an ASA registration
        # - It's unpaid
        # - It has 'early' in the title
        asa_regos = Registration.objects.filter(
            is_paid=False,
            meeting__slug='annual-meeting',
        )
        attendees_asa = Attendee.objects.filter(
            id__in=asa_regos.values('attendee_id')
        )

        # Generate the list of mail tuples
        mail_tuples = [
            ('ASA 2018 - Payment outstanding',
             self.email_body % (
                 a.given_names,
                 settings.ALLOWED_HOSTS[0] + reverse('register_splash'),
                 settings.GLOBAL_PAGE_TITLE,
             ),
             settings.REGISTRATION_EMAIL,
             [a.email, ])
            for a in attendees_asa
        ]

        # Send the email
        if len(mail_tuples) > 0:
            print('Sending mail to %d attendees' % len(mail_tuples))
            send_mass_mail(mail_tuples, fail_silently=False)
        else:
            print('No matching attendees - no emails sent')
