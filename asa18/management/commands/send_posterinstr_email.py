from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail
from django.utils.timezone import localtime
from django.conf import settings

from asa18.models import Presentation

from lxml import html

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('meeting', type=int)

    help = 'Send an email to all participants with posters, giving ' \
           'details of display, numbering etc.'

    email_body = "Dear %s,\n\n" \
                 "Further to our previous email, we're pleased to advise " \
                 "that your poster submission '%s' for ASA 2018 %s.\n\n" \
                 "Your poster should be printed no larger than A0 size. " \
                 "When you first arrive at the conference, please check in " \
                 "at the registration desk before hanging your poster. We " \
                 "will provide you with the necessary stationery to " \
                 "securely hang your poster, as well as direct you towards " \
                 "the appropriate poster board.\n\n" \
                 "On Tuesday and Wednesday, we will also have " \
                 "'Sparkler Sessions' - you will be able to prepare one " \
                 "slide and have one minute to talk about your poster. " \
                 "Poster numbers 1 - 15 will be on Tuesday, and the rest " \
                 "will be on Wednesday.\n\n" \
                 "Regards,\n" \
                 "%s LOC"

    def handle(self, *args, **options):
        # Get all the presentations that:
        # - Are talks
        # - Are currently flagged as accepted
        accepted_posters = Presentation.objects.filter(
            status='a',
            type='p',
            meeting=options['meeting'],
            # presenter__family_name__iexact='tucker',
        )

        # Generate the list of mail tuples
        mail_tuples = [
            ('ASA 2018 - Poster display information',
             self.email_body % (
                 t.presenter.given_names,
                 t.title,
                 'has been assigned ID %s' % t.generate_id() if t.id_no else
                 'has yet to be assigned an ID number. We will advise you of '
                 'your poster number when you check in at the registration '
                 'desk',
                 settings.GLOBAL_PAGE_TITLE,
             ),
             settings.REGISTRATION_EMAIL,
             [t.presenter.email, ])
            for t in accepted_posters
        ]

        # Send the email
        if len(mail_tuples) > 0:
            print('Sending information mail to %d poster presenters' %
                  len(mail_tuples))
            send_mass_mail(mail_tuples, fail_silently=False)
        else:
            print('No matching posters - no emails sent')
