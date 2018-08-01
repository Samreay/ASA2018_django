from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail
from django.utils.timezone import localtime
from django.conf import settings

from asa18.models import Presentation

from lxml import html

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('meeting', type=int)

    help = 'Send an email to all participants with scheduled talks, ' \
           'detailing when their talk is scheduled.'

    email_body = "Dear %s,\n\n" \
                 "Further to our previous email regarding your talk at %s, " \
                 "we are pleased to inform you of the scheduling of your " \
                 "talk: \n" \
                 "Time: %s\n" \
                 "Session: %s\n" \
                 "Location: %s\n" \
                 "Session chair: %s\n" \
                 "\n " \
                 "If you have any concerns with the scheduling of your talk, " \
                 "please contact us (%s) ASAP.\n\n" \
                 "We have included you talk abstract and title below for " \
                 "your reference.\n\n" \
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
            type='t',
            meeting=options['meeting'],
            time_start__isnull=False,
            time_end__isnull=False,
        )

        # Generate the list of mail tuples
        mail_tuples = [
            ('ASA 2018 - Talk accepted',
             self.email_body % (
                 t.presenter.given_names,
                 'ASA 2018',
                 '%s - %s' % (localtime(t.time_start).strftime(
                     '%A %d %B, %I:%M%p'),
                              localtime(t.time_end).strftime(
                                  '%I:%M%p')),
                 '%s' % 'TBD' if not t.session else '%s %s' % (
                     t.session.title,
                     '(%s)' % t.session.blurb if t.session.blurb else '',
                 ),
                 '%s' % 'TBD' if not t.session or not t.session.location
                 else '%s' % (
                     t.session.location if t.session.location else 'TBD'
                 ),
                 '%s' % 'TBD' if not t.session or not t.session.chair
                 else '%s' % (
                     t.session.chair.full_name() if t.session.chair else 'TBD'
                 ),
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
            print('Sending scheduled mail to %d talk presenters' %
                  len(mail_tuples))
            send_mass_mail(mail_tuples, fail_silently=False)
        else:
            print('No scheduled talks - no emails sent')
