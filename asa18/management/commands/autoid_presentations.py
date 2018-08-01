from django.core.management.base import BaseCommand, CommandError

from asa18.models import Presentation, Meeting
from asa18.helpers import alphanum_key

class Command(BaseCommand):
    help = 'Auto-id presentations of a particular meeting and type'

    def add_arguments(self, parser):
        parser.add_argument('meeting', type=int)
        parser.add_argument('type', type=str)

    def handle(self, *args, **options):
        # Get the meeting
        meeting = Meeting.objects.get(id=options['meeting'])
        # Get the Presentations
        presentations = Presentation.objects.filter(
            meeting=meeting,
            type=options['type'],
        )
        # Blank the id_no
        presentations.update(id_no=None)
        for p in presentations:
            p.save()

        # Filter the presentations down to the accepted ones
        presentations = presentations.filter(status='a')
        # If type=talk, re-order by time_start, session, time_end
        if options['type'] == 't':
            # presentations.order_by('time_start', 'session', 'time_end')
            presentations = list(presentations)
            presentations.sort(key=lambda x: (x.time_start,
                                              x.session.time_start if
                                              x.session else None,
                                              alphanum_key(x.session.title) if
                                              x.session else
                                              None,
                                              x.session.time_end if
                                              x.session else None,
                                              x.time_end,
                                              ))
        # If type=talk, re-order by author family name, given name, then title
        elif options['type'] == 'p':
            presentations.order_by('presenter__family_name',
                                   'presenter__given_names',
                                   'title', )

        # Execute the numbering
        i = 1
        for p in presentations:
            p.id_no = i
            p.save()
            i += 1

        print('Auto-magically generated IDs for %d %ss in %s' % (
            len(presentations) if isinstance(presentations, list)
            else presentations.count(),
            [_[1] for _ in Presentation.TYPE_CHOICES if
             _[0] == options['type']][0],
            meeting.abbrv,
        ))
