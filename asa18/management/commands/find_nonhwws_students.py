from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail, send_mail

from asa18.models import Registration, Attendee

class Command(BaseCommand):
    help = 'Locate all students attending ASA, but not HWWS'

    def handle(self, *args, **options):
        # Get all the attendees who:
        # - Have an ASA registration
        # - It's unpaid
        # - It has 'early' in the title
        asa_regos = Registration.objects.filter(
            meeting__slug='annual-meeting',
        )
        hwws_regos = Registration.objects.filter(
            meeting__slug='harley-wood',
        )

        attendees_slack = Attendee.objects.filter(
            id__in=asa_regos.values('attendee_id')
        ).exclude(
            id__in=hwws_regos.values('attendee_id')
        ).filter(
            academic_level__in=['undergrad', 'masters', 'phd', ]
        )

        print('Possibly truant students:')
        for a in attendees_slack:
            print(a.__unicode__())
