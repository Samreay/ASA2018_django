# These are the main models (e.g. meeting, rego options etc.) for asa18

from django.db import models, IntegrityError
from django.db.models import Sum, Q, Min, Max
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.text import slugify
from django.core.validators import RegexValidator
import django.core.mail
from tinymce import models as tinymce_models
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from multiselectfield import MultiSelectField
from django_countries.fields import CountryField
import random
import string
import re
from decimal import Decimal
from datetime import tzinfo

import hashlib
import hmac

import settings
import urllib

#import unidecode

from django.conf import settings

from io import BytesIO

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, \
    TableStyle
from reportlab.lib.units import inch, pica
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors, enums

ATTENDEE_PK_LENGTH = 30

import re
import unicodedata

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def _generate_attendee_pk(length=ATTENDEE_PK_LENGTH):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for
                   _ in range(length))


class Meeting(models.Model):
    """
    Main model for holding top-level meeting information
    """

    # Model fields
    name = models.CharField(max_length=400, blank=False,
                            unique=True,
                            help_text='Full meeting name')
    abbrv = models.CharField(max_length=400, blank=False,
                             unique=True,
                             help_text='Abbreviated meeting name - '
                                       'avoid changing this once set!')
    slug = models.SlugField(blank=False, unique=True,
                            help_text='URL root for this meeting - often best '
                                      'to use the default that is '
                                      'auto-generated from the abbreviation')
    date_start = models.DateField(blank=False,
                                  unique=False,
                                  help_text='First day of meeting')
    date_end = models.DateField(blank=True,
                                unique=False,
                                help_text='Last day of meeting '
                                          '(leave blank for a single-day '
                                          'meeting)')
    blurb = models.CharField(max_length=400, blank=True,
                             help_text='*Short* blurb about meeting')
    description = RichTextUploadingField(help_text='Detailed description of '
                                                     'meeting - you can '
                                                     'include sections '
                                                     'covering all manner '
                                                     'of things, and load in '
                                                     'images/Google maps '
                                                     'frames etc.')
    # Formatting fields
    distinct_color = ColorField(blank=False, default='#000000',
                                help_text='Choose a distinctive colour to '
                                          'differentiate this meeting from '
                                          'others. It should *not* be red or '
                                          'red-like, and should be an '
                                          'appropriate colour for having white '
                                          'text laid over it.')

    # Control fields
    publish_diversity = models.BooleanField(null=False, default=False,
                                            help_text='Check this to activate '
                                                      'the automated diversity '
                                                      'reporting')
    publish_attendees = models.BooleanField(null=False, default=False,
                                            help_text='Check this to activate '
                                                      'the automated attendee '
                                                      'reporting')
    accept_abstracts = models.BooleanField(null=False, default=True,
                                           help_text='Does this meeting accept '
                                                     'abstracts from public '
                                                     'registrations?')
    abstract_date = models.DateTimeField(null=True, blank=True,
                                         help_text='What is the end datetime '
                                                   'for accepting abstracts? '
                                                   'Leave blank to enforce '
                                                   'no date. '
                                                   '(Note this is distinct '
                                                   'from registration dates)')
    program_release_date = models.DateTimeField(blank=True, null=True,
                                                help_text="Date and time at "
                                                          "which to release "
                                                          "the meeting "
                                                          "program. Leave "
                                                          "blank to not "
                                                          "release the program")
    program_hardcopy = models.FileField(blank=True, null=True,
                                        help_text='Upload a hardcopy of the '
                                                  'program here for download',
                                        upload_to='prog/%Y/%m/%d/')

    def clean(self, *args, **kwargs):
        # Check that date_end is after date_start
        if self.date_end is not None:
            if self.date_end <= self.date_start:
                raise ValidationError('date_end must be after date_start (set '
                                      'date_end to None '
                                      'for a single-day meeting')
        # Super any higher-level clean methods
        super(Meeting, self).clean(*args, **kwargs)

    def __unicode__(self):
        return self.abbrv

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('meeting_splash', args=[
            str(self.slug),
        ])

    def get_absolute_event_url(self):
        from django.core.urlresolvers import reverse
        return reverse('event_index', args=[
            str(self.slug),
        ])

    def get_absolute_policy_url(self):
        from django.core.urlresolvers import reverse
        return reverse('policy', args=[
            str(self.slug),
        ])

    def get_absolute_news_url(self):
        from django.core.urlresolvers import reverse
        return reverse('news_index_meeting', args=[
            str(self.slug),
        ])

    def get_absolute_prize_url(self):
        from django.core.urlresolvers import reverse
        return reverse('prize_index', args=[
            str(self.slug),
        ])

    def get_absolute_sponsors_url(self):
        from django.core.urlresolvers import reverse
        return reverse('sponsors', args=[
            str(self.slug),
        ])

    def get_absolute_hpc_helpdesk_url(self):
        from django.core.urlresolvers import reverse
        return reverse('hpc_helpdesk', args=[
            str(self.slug),
        ])

    def get_absolute_presenter_info_url(self):
        from django.core.urlresolvers import reverse
        return reverse('presenter_information', args=[
            str(self.slug),
        ])

    def get_absolute_program_url(self):
        from django.core.urlresolvers import reverse
        return reverse('program', args=[
            str(self.slug),
        ])

    def get_absolute_posters_url(self):
        from django.core.urlresolvers import reverse
        return reverse('posters', args=[
            str(self.slug),
        ])

    def get_absolute_participants_url(self):
        from django.core.urlresolvers import reverse
        return reverse('participants', args=[
            str(self.slug),
        ])

    def get_accepted_posters(self):
        posters = Presentation.objects.filter(
            meeting=self,
            status='a',
            type='p'
        )
        return posters

    def get_accepted_talks(self):
        talks = Presentation.objects.filter(
            meeting=self,
            status='a',
            type='t'
        )
        return talks

    def has_accepted_posters(self):
        if self.get_accepted_posters().count() > 0:
            return True
        return False

    def has_accepted_talks(self):
        if self.get_accepted_talks().count() > 0:
            return True
        return False

    def is_rego_open(self, now=timezone.now()):
        # Determine if registration is open or not for this meeting
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
        )
        if rego_opts.count() == 0:
            return False
        open_date = localtime(
            rego_opts.aggregate(open_date=Min('opens'))['open_date'])
        close_date = localtime(
            rego_opts.aggregate(close_date=Max('closes'))['close_date'])
        if now > open_date and now < close_date:
            return True
        return False

    def get_rego_opens(self):
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
        )
        if rego_opts.count() == 0:
            return None
        open_date = localtime(
            rego_opts.aggregate(open_date=Min('opens'))['open_date'])
        return open_date

    def get_opened_rego_list(self):
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
            opens__lte=timezone.now(),
            closes__gt = timezone.now()
        ).order_by('opens')

        return rego_opts

    def get_closed_rego_list(self):
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
            opens__lte=timezone.now(),
            closes__lte = timezone.now()
        ).order_by('opens')

        return rego_opts

    def get_to_open_rego_list(self):
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
            opens__gte=timezone.now()
        ).order_by('opens')

        return rego_opts

    def has_rego_closed(self, now=timezone.now()):
        # Determine if registration is open or not for this meeting
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
        )
        if rego_opts.count() == 0:
            return False
        close_date = localtime(
            rego_opts.aggregate(close_date=Max('closes'))['close_date'])
        if now > close_date:
            return True
        return False

    def get_rego_closes(self):
        rego_opts = RegoOption.objects.filter(
            meeting=self,
            public=True,
        )
        if rego_opts.count() == 0:
            return None
        close_date = localtime(
            rego_opts.aggregate(close_date=Max('closes'))['close_date'])
        return close_date

    def generate_attendee_gender(self, threshold=0.015, hard_lim=3,
                                 presentation_type=None):
        """
        Form a Chart.js compliant datasets object re: gender distribution for
        this meeting
        """
        if presentation_type is not None:
            attendees = Attendee.objects.filter(
                presentation__type__in=[presentation_type, ],
                presentation__status__in=['a', ],
                presentation__meeting__in=[self, ]
            ).distinct()
        else:
            attendees = Attendee.objects.all()
        attendees = attendees.filter(
            registration__meeting__in=[self, ]
        )

        if attendees.count() == 0:
            return ([], [], )

        count_dict = dict()
        count_tot = attendees.count()
        for gender in Attendee.GENDER_CHOICES:
            count_dict[gender[1]] = attendees.filter(gender=gender[0]).count()

        # If the count for any gender group is less than the threshold
        # percentage, combine it into a super-group
        supergroup_names = []
        supergroup_count = 0
        for gender in count_dict.keys():
            if (float(count_dict[gender]) / float(count_tot) <
                    threshold) or (count_dict[gender] < hard_lim):
                supergroup_names.append(gender)
                supergroup_count += count_dict[gender]
                count_dict[gender] = 0
        if supergroup_count > 0:
            count_dict[', '.join(supergroup_names)] = supergroup_count

        # Strip out any groups under the hard_lim
        count_dict = {k: v for k, v in count_dict.items() if
                      v >= hard_lim and float(v)/float(count_tot) >= threshold}

        return (count_dict.keys(), count_dict.values(), )

    def generate_attendee_level(self, threshold=0.015, hard_lim=3,
                                presentation_type=None):
        """
        Form a Chart.js compliant datasets object re: gender distribution for
        this meeting
        """
        if presentation_type is not None:
            attendees = Attendee.objects.filter(
                presentation__type__in=[presentation_type, ],
                presentation__status__in=['a', ],
                presentation__meeting__in=[self, ]
            ).distinct()
        else:
            attendees = Attendee.objects.all()
        attendees = attendees.filter(
            registration__meeting__in=[self, ]
        )

        if attendees.count() == 0:
            return ([], [], )

        count_dict = dict()
        count_tot = attendees.count()
        for level in Attendee.ACADEMIC_LEVEL_CHOICES:
            count_dict[level[1]] = attendees.filter(
                academic_level=level[0]).count()

        # If the count for any gender group is less than the threshold
        # percentage, combine it into a super-group
        supergroup_names = []
        supergroup_count = 0
        for level in count_dict.keys():
            if (float(count_dict[level]) / float(count_tot) <
                    threshold) or (count_dict[level] < hard_lim):
                supergroup_names.append(level)
                supergroup_count += count_dict[level]
                count_dict[level] = 0
        if supergroup_count > 0:
            count_dict[', '.join(supergroup_names)] = supergroup_count

        # Strip out any groups under the hard_lim
        count_dict = {k: v for k, v in count_dict.items() if
                      v >= hard_lim and float(v)/float(count_tot) >= threshold}

        return (count_dict.keys(), count_dict.values(), )


class Policy(models.Model):
    """
    Policies/procedures etc.
    """
    class Meta:
        verbose_name_plural = 'policies'
        ordering = ('name', )

    # Model fields
    meetings = models.ManyToManyField(Meeting, blank=False,
                                      help_text='Please select all meetings '
                                                'this policy applies to')
    name = models.CharField(max_length=400, blank=False,
                            unique=True,
                            help_text='Policy title')
    slug = models.SlugField(max_length=100,
                            help_text='We recommend you use the auto-generated '
                                      'default for this field')
    content = RichTextUploadingField(blank=False,
                                       help_text='Policy content')

    def __unicode__(self):
        return self.name


class Sponsor(models.Model):
    """
    Describes a body sponsoring a meeting
    """

    # Model fields
    name = models.CharField(max_length=300, blank=False, null=False,
                            unique=True,
                            help_text='Sponsor name')
    url = models.URLField(help_text='Sponsor website')
    logo = models.ImageField(help_text='Upload a sponsor logo here - the '
                                       'closer to square the image is, the '
                                       'better. No larger than 500px should be '
                                       'necessary.')
    meetings = models.ManyToManyField(Meeting)

    def __unicode__(self):
        return self.name


class News(models.Model):
    """
    For holding updated news/information about a meeting(s)
    """
    class Meta:
        verbose_name = 'news item'
        ordering = ('-pub_date', )

    title = models.CharField(max_length=100, blank=False, null=False,
                             unique=True)
    slug = models.SlugField(max_length=100,
                            help_text='Recommend leaving this as the auto-'
                                      'generated default')
    meetings = models.ManyToManyField(Meeting, blank=True,
                                      # null=True,
                                      help_text='Please select all meetings '
                                                'this news item pertains to')
    body = RichTextUploadingField(blank=False, null=False)

    pub_date = models.DateTimeField(blank=True, null=True,
                                    help_text='You can back-date or '
                                              'future-date news items to have '
                                              'them appear earlier on the '
                                              'site, or have them be released '
                                              'at a particular time')

    def __unicode__(self):
        return '%s (%s)' % (self.title,
                            self.pub_date.astimezone(
                                # timezone(settings.TIME_ZONE)
                                timezone.get_current_timezone()
                            ).strftime(
                                '%Y-%m-%d %H:%M'))

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('news', args=[
            str(self.slug),
        ])

    def get_absolute_meeting_url(self, meeting_slug):
        from django.core.urlresolvers import reverse
        return reverse('news_meeting', args=[
            meeting_slug,
            str(self.slug),
        ])



class Banner(models.Model):
    """
    Site banner image
    """
    img = models.ImageField(blank=False, null=False,
                            help_text='Should be an image 5120x600 at minimum, '
                                      'with the most interesting content '
                                      'centered vertically')
    vert_position = models.DecimalField(max_digits=4, decimal_places=1,
                                        blank=True, null=True,
                                        default=None,
                                        help_text='Set percentage value here '
                                                  'for vertical positioning '
                                                  'of banner image. Leave '
                                                  'blank to use default (50).',
                                        validators=[MinValueValidator(0.),
                                                    MaxValueValidator(100.), ]
                                        )

    def __unicode__(self):
        return self.img.name


class AttendeeQuerySet(models.QuerySet):
    def diversity_statistics(self, first='gender', second='academic_level'):
        """
        TERMINAL function - returns a sunburst CSV of diversity
        statistics
        """
        relevant_fields = ['gender', 'academic_level', 'years_since_phd', ]
        if first not in relevant_fields:
            raise ValueError('Specified first field must be one of %s' %
                             ', '.join(relevant_fields))
        if second not in relevant_fields:
            raise ValueError('Specified first field must be one of %s' %
                             ', '.join(relevant_fields))
        third = [_ for _ in relevant_fields if _ != first and _ != second][0]

        user_stats = self.values(*relevant_fields)
        return user_stats


class Attendee(models.Model):
    """
    Details an attendee to a meeting.
    """

    objects = AttendeeQuerySet.as_manager()

    class Meta:
        ordering = ['family_name', 'given_names']

    ACADEMIC_LEVEL_CHOICES = (
        ('undergrad', 'Undergraduate/honours student'),
        ('masters', 'Masters student'),
        ('phd', 'PhD student'),
        ('postdoc', 'Postdoctoral Fellow'),
        ('fellow', 'Research Fellow'),
        ('faculty', 'Faculty'),
        ('emeritus', 'Emeritus faculty'),
        ('professional', 'Professional staff'),
        ('other', 'Other'),
    )
    ACADEMIC_LEVEL_CHOICES_DICT = {
        'undergrad': 'Undergraduate/honours student',
        'masters': 'Masters student',
        'phd': 'PhD student',
        'postdoc': 'Postdoctoral Fellow',
        'fellow': 'Research Fellow',
        'faculty': 'Faculty',
        'emeritus': 'Emeritus faculty',
        'professional': 'Professional staff',
        'other': 'Other'
    }

    NAME_ORDER_CHOICES = (
        ('w', 'GivenName FAMILYNAME'),
        ('e', 'FAMILYNAME GivenName'),
    )

    STATE_CHOICES = (
        ('a', 'ACT'),
        ('n', 'NSW'),
        ('t', 'NT'),
        ('q', 'QLD'),
        ('s', 'SA'),
        ('h', 'TAS'),
        ('v', 'VIC'),
        ('w', 'WA'),
        ('x', 'N/A'),
    )


    # Model fields
    # Basic fields
    id = models.CharField(max_length=30, blank=False, null=False,
                          editable=False, primary_key=True)
    given_names = models.CharField(max_length=100, blank=False,
                                   help_text='Your given name(s)')
    family_name = models.CharField(max_length=50, blank=False,
                                   help_text='Your family name (i.e. by which '
                                             'your publications are referenced)'
                                             '')
    name_order = models.CharField(max_length=1, blank=False,
                                  help_text='In which order should your names '
                                            'be rendered?',
                                  choices=NAME_ORDER_CHOICES,
                                  default=NAME_ORDER_CHOICES[0][0])
    email = models.EmailField(blank=False, unique=True)
    phone = models.CharField(max_length=16,
                             validators=[RegexValidator(
                                 regex=r'^\+?\d{7,15}$',
                                 message='Please use international dialling code if registering from overseas'), ],
                             help_text="Please use international dialling code if registering from overseas")
    address = models.CharField(max_length=300, blank=False, null=False,
                               default='',
                               help_text='Required for invoicing')
    city = models.CharField(max_length=100, blank=True, null=False,
                            default='',
                            help_text='Suburb/town/city')
    state = models.CharField(max_length=1, blank=False, null=False,
                             choices=STATE_CHOICES,
                             default=STATE_CHOICES[-1][0])
    postcode = models.CharField(max_length=6, blank=False, null=False,
                                default='')
    country = CountryField()

    institution = models.CharField(max_length=100, blank=False,
                                   help_text='Please write the full name of '
                                             'your home institution (no '
                                             'abbreviations)')
    academic_level = models.CharField(max_length=15,
                                      choices=ACADEMIC_LEVEL_CHOICES,
                                      blank=False,
                                      help_text='Please select your academic '
                                                'level/appointment. This is '
                                                '*required* to provide you '
                                                'the appropriate registration '
                                                'options')
    is_asa_member = models.BooleanField(null=False, default=False,
                                        help_text='Tick if you are a current '
                                                  'ASA member')
    is_nz_astro = models.BooleanField(null=False, default=False,
                                      help_text='Tick if you are *not* an ASA '
                                                'member, but you are based in '
                                                'New Zealand')

    # Diversity information fields
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('x', 'Intersex'),
        ('o', 'Other'),
        ('z', 'Do not disclose')
    )
    YEARS_SINCE_PHD_CHOICES = (
        ('0-3', '0 - 3 years'),
        ('3-6', '3 - 6 years'),
        ('6-10', '6 - 10 years'),
        ('10-15', '10 - 15 years'),
        ('15+', '15+ years'),
        ('NA', 'Not applicable/awarded'),
        ('z', 'Do not disclose')
    )
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              blank=False,
                              help_text="Please select the gender you identify "
                                        "as, or 'Do not disclose' if you do "
                                        "not wish to provide this information")
    years_since_phd = models.CharField(max_length=5,
                                       choices=YEARS_SINCE_PHD_CHOICES,
                                       blank=False,
                                       # default=YEARS_SINCE_PHD_CHOICES[-1][0],
                                       help_text="Please select how many years "
                                                 "it has been since you were "
                                                 "awarded your PhD, or 'Do not"
                                                 " disclose' if you do not "
                                                 "wish to provide this "
                                                 "information")

    # Organizer-specific information
    is_organizer = models.BooleanField(blank=False, default=False,
                                       help_text='Is this person a conference '
                                                 'organizer?')
    socs = models.ManyToManyField(Meeting, blank=True,
                                  help_text='Please select the meeting(s) this '
                                            'person is on the SOC for',
                                  related_name='meetings_soc')
    locs = models.ManyToManyField(Meeting, blank=True,
                                  help_text='Please select the meeting(s) this '
                                            'person is on the SOC for',
                                  related_name='meetings_loc')

    def full_name(self, capitalize_family=False):
        """
        Attendee full name
        """
        return '%s %s' % ((self.given_names,
                           self.family_name.upper() if capitalize_family else
                           self.family_name,
                           ) if self.name_order == 'w' else
                          (self.family_name.upper() if capitalize_family else
                           self.family_name,
                           self.given_names,
                           ))

    def membership_pretty(self):
        if self.is_asa_member:
            return 'ASA Member'
        elif self.is_nz_astro:
            return 'NZ Astronomer'
        return ''

    def address_str(self):
        """
        Nicely formatted HTML address
        """
        return '%s\n%s, %s %s, %s' % (self.address,
                                      self.city,
                                      self.get_state_display()+',' if
                                      self.state != 'x' else '',
                                      self.country.name,
                                      self.postcode)

    def address_html(self):
        """
        Nicely formatted HTML address
        """
        return '%s<br />%s, %s %s, %s' % (self.address,
                                          self.city,
                                          self.get_state_display()+',' if
                                          self.state != 'x' else '',
                                          self.country.name,
                                          self.postcode)

    def academic_level_formatted(self):
        return '%s' % (self.ACADEMIC_LEVEL_CHOICES_DICT[self.academic_level])

    def __unicode__(self):
        return '%s (%s)' % (self.full_name(capitalize_family=True),
                            self.email)

    def generate_abstract_key(self, dt=timezone.now()):
        """
        Generate a 'secret key' to allow users to access the abstract
        editing system
        """
        # The encrypt sequence is:
        # Django secret key as the key
        # PK as the first string
        # Date string as the second string
        hashed = hmac.new(settings.SECRET_KEY,
                          self.pk,
                          hashlib.sha1)
        hashed.update(dt.strftime('%y%m%d'))
        repl_pattern = re.compile('[\W]+')
        return repl_pattern.sub('',
                                hashed.digest().encode('base64').rstrip('\n'))

    def generate_abstract_email(self, dt=timezone.now(), reqobj=None):
        """
        Generate a plain-text email body to send to a person to provide their
        abstract editing key
        """
        from django.core.urlresolvers import reverse

        get_params = urllib.urlencode({
            'key': self.generate_abstract_key(dt=dt),
            'email': self.email,
        })

        email_body = ''
        email_body += 'Hello %s,' % self.full_name(capitalize_family=False)
        email_body += '\n\n'
        email_body += 'To add/edit/withdraw your abstracts, please go to this ' \
                      'URL:\n'
        email_body += '%s?%s' % (reverse('edit_abstracts') if reqobj is None
                                 else reqobj.build_absolute_uri(
            reverse('edit_abstracts')),
                                 get_params)
        email_body += '\n\n'
        email_body += 'Please note that this URL will expire at *midnight ' \
                      'tonight* AEST. Please ensure you have completed all ' \
                      'editing by that time. '

        email_body = email_body.replace('http://web/', 'http://asa2018.swin.edu.au/')

        return email_body

    def generate_check_email(self, dt=timezone.now(), reqobj=None):
        """
        Generate a plain-text email body to send to a person to provide their
        abstract editing key
        """
        from django.core.urlresolvers import reverse

        get_params = urllib.urlencode({
            'key': self.generate_abstract_key(dt=dt),
            'email': self.email,
        })

        email_body = ''
        email_body += 'Hello %s,' % self.full_name(capitalize_family=False)
        email_body += '\n\n'
        email_body += 'To check your registration, and pay any outstanding ' \
                      'costs, please go to this ' \
                      'URL:\n'
        email_body += '%s?%s' % (reverse('check_rego') if reqobj is None
                                 else reqobj.build_absolute_uri(
            reverse('check_rego')),
                                 get_params)
        email_body += '\n\n'
        email_body += 'Please note that this URL will expire at *midnight ' \
                      'tonight* AEST. '
        
        email_body = email_body.replace('http://web/', 'http://asa2018.swin.edu.au/')

        return email_body

    def clean(self):
        super(Attendee, self).clean()
        # Make sure that only one of is_asa_member or is_nz_astro is set
        if self.is_asa_member and self.is_nz_astro:
            raise ValidationError('Please only select yourself as an ASA '
                                  'member, OR as a New Zealand-based '
                                  'astronomer. If you are both, select '
                                  'ASA member')
        # Make sure state if None is country isn't Australia
        if self.country.code != 'AU':
            self.state = self.STATE_CHOICES[-1][0]
        # Force students to have PhD not awarded
        if self.academic_level in ['undergrad', 'masters', 'phd', ] and \
                        self.years_since_phd != 'z':
            self.years_since_phd = 'NA'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = _generate_attendee_pk()
        saved = False
        while not saved:
            try:
                super(Attendee, self).save(*args, **kwargs)
                saved = True
            except IntegrityError:
                self.id = _generate_attendee_pk()
        return self


class RegoOption(models.Model):
    """
    Conference registration options
    """
    class Meta:
        verbose_name = 'registration option'
        ordering = ['closes', 'opens', 'cost']

    # Model fields
    meeting = models.ForeignKey(Meeting, blank=False,
                                help_text='Meeting this option is for')
    name = models.CharField(max_length=400, blank=False,
                            unique=True,
                            help_text='Full option name & details '
                                      '(e.g. open to whom, if early bird, '
                                      'etc.)')
    public = models.BooleanField(null=False, default=True,
                                 help_text='De-select this option to make this '
                                           'registration an internal use-only '
                                           'option')
    asa_only = models.BooleanField(null=False, default=False,
                                   help_text='Tick this to restrict this '
                                             'option to ASA members only')
    nz_only = models.BooleanField(null=False, default=False,
                                  help_text='Tick this to restrict this '
                                            'option to NZ astronomer')
    available_to = MultiSelectField(choices=Attendee.ACADEMIC_LEVEL_CHOICES)
    cost = models.DecimalField(max_digits=6, decimal_places=2,
                               blank=False,
                               help_text='Include GST if required')
    opens = models.DateTimeField(blank=False,
                                 help_text='Local time to open rego option')
    closes = models.DateTimeField(blank=False,
                                  help_text='Local time to close option')

    def clean(self, *args, **kwargs):
        # Check that closes is after opens
        if self.closes <= self.opens:
            raise ValidationError('closes must be after opens')
        # Super any higher-level clean methods
        super(RegoOption, self).clean(*args, **kwargs)

    def __unicode__(self):
        return '%s - %s ($%.2fAUD)' % (self.meeting.abbrv, self.name,
                                       self.cost, )


class Registration(models.Model):
    """
    Registration which attaches a person to a particular meeting and
    registration option
    """
    class Meta:
        unique_together = ['attendee', 'meeting', ]
        ordering = ['attendee', 'meeting']

    attendee = models.ForeignKey(Attendee, unique=False, null=False,
                                 blank=False)
    meeting = models.ForeignKey(Meeting, unique=False, null=False, blank=False)
    meeting_rego = models.ForeignKey(RegoOption, unique=False, null=True,
                                     blank=True,
                                     default=None)
    is_paid = models.BooleanField(blank=False, default=False)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s - %s' % (self.meeting.abbrv,
                            self.attendee.full_name())

    def clean(self):
        try:
            if self.meeting_rego.meeting != self.meeting:
                raise ValidationError('Registration option is not for the '
                                      'given meeting!')
        except:
            raise ValidationError('Please select a valid registration option.')


class Event(models.Model):
    """
    Describes a special event (e.g. conference dinner, tour etc.) attached to a
    meeting
    """
    class Meta:
        ordering = ['time_start', 'time_end', ]

    # Model fields
    name = models.CharField(max_length=200, blank=False,
                            help_text='Event name')
    slug = models.SlugField(max_length=100, blank=False, unique=True,
                            help_text='Recommend you use auto-generated value')
    meetings = models.ManyToManyField(Meeting, blank=False,
                                      help_text='Select all meetings this '
                                                'event is attached to')
    location = models.CharField(blank=True, max_length=300,
                                help_text='Address or other simple location '
                                          'of the event (you can add more '
                                          'description, Google Maps etc. in '
                                          'the event description. You can wrap '
                                          'your description in link tags if '
                                          'you do want to link to Google Maps '
                                          'from here.')
    description = RichTextUploadingField(blank=False)
    time_start = models.DateTimeField(blank=False)
    time_end = models.DateTimeField(blank=False)
    dietary_required = models.BooleanField(blank=False, default=False)

    rego_closes = models.DateTimeField(blank=True, null=True,
                                       help_text='Leave blank to use the rego '
                                                 'opening date of the related '
                                                 'event(s)')

    publication_date = models.DateTimeField(blank=False,
                                            help_text='Time this event should '
                                                      'be made publically '
                                                      'available for viewing. '
                                                      'Note this does *not* '
                                                      'affect registrations.')

    def clean(self, *args, **kwargs):
        # Check start date is before end date
        if self.time_start >= self.time_end:
            raise ValidationError('End time must be after start time!')
        super(Event, self).clean()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('event', args=[
            str(self.meetings.all()[0].slug),
            str(self.slug),
        ])

    def get_relative_url(self):
        return '%s/' % self.slug

    def compute_rego_closes(self):
        """
        Returns the effective close of registration date if none is defined
        """
        rego_closes = RegoOption.objects.filter(
            meeting__in=self.meetings.all()
        ).aggregate(models.Max('closes'))['closes__max']
        return rego_closes

    def get_rego_closes(self):
        """
        Return the defined rego closes time if exists, otherwise compute it
        """
        if self.rego_closes:
            return self.rego_closes
        return self.compute_rego_closes()

    def title(self):
        """
        Allows for a common template name to call both event and session titles
        """
        return self.name


class EventOption(models.Model):
    """
    Conference registration options
    """
    class Meta:
        verbose_name = 'event sign-up option'
        unique_together = ['event', 'name', ]

    # Model fields
    event = models.ForeignKey(Event, blank=False,
                              help_text='Meeting this option is for')
    name = models.CharField(max_length=400, blank=False,
                            unique=False,
                            help_text='Full option name & details '
                                      '(e.g. open to whom, if early bird, '
                                      'etc.)')
    public = models.BooleanField(null=False, default=True,
                                 help_text='De-select this option to make this '
                                           'event an internal use-only '
                                           'option')
    cost = models.DecimalField(max_digits=6, decimal_places=2,
                               blank=False,
                               help_text='Include GST if required')
    extra_guests = models.IntegerField(null=False, default=0,
                                       help_text='How many extra guests this '
                                                 'event option includes')

    def __unicode__(self):
        return '%s - %s ($%.2f)' % (self.event.name,
                                    self.name, self.cost, )


class EventRegistration(models.Model):
    """
    Registration which attaches a person to a particular meeting and
    registration option
    """
    class Meta:
        unique_together = ['attendee', 'event', ]
        ordering = ['event', 'event_option', 'attendee']

    attendee = models.ForeignKey(Attendee, unique=False, blank=False)
    event = models.ForeignKey(Event, unique=False, blank=False)
    event_option = models.ForeignKey(EventOption, unique=False, blank=False)
    is_paid = models.BooleanField(null=False, default=False)
    extra_comments = models.CharField(blank=True, default='',
                                      max_length=300,
                                      help_text="Please add any extra comments "
                                                "regarding your registration "
                                                "here")

    def clean(self, *args, **kwargs):
        super(EventRegistration, self).clean(*args, **kwargs)
        # Check that the event and event_option match
        if self.event != self.event_option.event:
            raise ValidationError('The event_option specified must be for '
                                  'the specified event')

    def __unicode__(self):
        return '%s - %s - %s' % (self.event.name, self.attendee.family_name,
                                 self.event_option.name, )


class Payment(models.Model):
    """
    Groups LineItems together into a single payment amount which can be passed
    on to OneStop
    """
    order_id = models.CharField(max_length=70, blank=False, primary_key=True,
                                editable=False)
    attendee = models.ForeignKey(Attendee, null=False)
    cost = models.DecimalField(max_digits=6, decimal_places=2,
                               blank=False, null=True)
    is_paid = models.BooleanField(null=False, default=False, editable=True)
    invoice_no = models.CharField(max_length=60, unique=False, blank=True,
                                  editable=True)
    receipt_no = models.CharField(max_length=60, unique=False, blank=True,
                                  editable=True)
    created = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=6, decimal_places=2,
                                      blank=True, null=True)

    def compute_cost(self):
        cost = Decimal(0.)
        cost += sum([x.meeting_rego.meeting_rego.cost for x in
                     self.lineitem_set.all() if x.meeting_rego is not None])
        cost += sum([x.event_rego.event_option.cost for x in
                     self.lineitem_set.all() if x.event_rego is not None])
        return cost

    def clean(self):
        super(Payment, self).clean()
        # Make sure that a paid_at has been set if is_paid is True
        if self.is_paid and self.paid_at is None:
            raise ValidationError('You must set the paid_at datetime when '
                                  'setting is_paid to True')
        if self.paid_at is not None and not self.is_paid:
            raise ValidationError('You must not set paid_at unless is_paid '
                                  'is True')

    def generate_order_id(self, save=True):
        """
        Generate the recommended order_id
        """
        # print('Generating order_id')
        if self.created != None:
            self.order_id = '%s+%s'[:60] % (self.created.strftime('%d%m%y%H%M'),
                                            re.sub(
                                                r'[^a-zA-Z]', '',
                                                self.attendee.family_name.upper()
                                            ), )
        else:
            self.order_id = '%s+%s'[:60] % (timezone.localtime(
                    timezone.now(), timezone.get_current_timezone()).strftime('%d%m%y%H%M'),
                                            re.sub(
                                                r'[^a-zA-Z]', '',
                                                self.attendee.family_name.upper()
                                            ),)
        if save:
            while save:
                try:
                    # print('Attempting to save order_id')
                    self.save()
                    save = False
                except KeyError:
                    self.order_id += '1'

    def get_dict(self):
        """
        Return a dictionary of key, value pairs used to generate a OneStop URL
        """
        d = {}

        # Global config
        d['Tran-Type'] = settings.ONESTOP_TRAN_TYPE
        d['GLCode'] = settings.ONESTOP_GLCODE
        d['StoreID'] = settings.ONESTOP_STOREID

        # Order specifics
        d['OrderID'] = self.order_id
        description = '; '.join(
            ['%s: %s' % (l.meeting_rego.meeting.name,
                         l.meeting_rego.meeting_rego.name) for l in
             self.lineitem_set.all() if
             l.meeting_rego is not None] +
            ['%s: %s' % (l.event_rego.event.name,
                         l.event_rego.event_option.name) for l in
             self.lineitem_set.all() if
             l.event_rego is not None]
        )
        d['Description'] = description
        d['UnitAmountIncTax'] = self.cost
        d['TaxCode'] = 'GS'  # Assume all items attract GST

        # Personal info
        d['CartName'] = self.attendee.full_name()
        d['Address_Line_1'] = self.attendee.address
        d['Address_Line_3'] = self.attendee.city
        d['AustStates'] = self.attendee.get_state_display() if \
            self.attendee.state != Attendee.STATE_CHOICES[-1][0] else ''
        d['Address_Postcode'] = self.attendee.postcode
        d['Address_Line_5'] = self.attendee.country.name
        d['Phone'] = self.attendee.phone
        d['Email'] = self.attendee.email

        return d

    def generate_summary_string(self):
        summary_str = 'REGISTRATION SUMMARY\n'
        summary_str += '-----\n\n'

        summary_str += self.attendee.address_str()
        summary_str += '\n%s\n%s' % (
            self.attendee.phone,
            self.attendee.email,
        )
        summary_str += '\n\n'

        summary_str += '%s\n%s\n%s' % (
            self.attendee.get_academic_level_display(),
            self.attendee.institution,
            self.attendee.membership_pretty()
        )

        summary_str += '\n\n'

        # Step through each meeting and add the relevant information
        meeting_regos = self.lineitem_set.filter(meeting_rego__isnull=False)
        if meeting_regos.count() > 0:
            summary_str += 'Meetings\n'
            summary_str += '-----\n'
            for l in meeting_regos:
                summary_str += '%s: %s - $%.2fAUD\n' % (
                    l.meeting_rego.meeting.name,
                    l.meeting_rego.meeting_rego.name,
                    float(l.meeting_rego.meeting_rego.cost),
                )
            summary_str += '\n'
        # Step through each event and add the relevant information
        event_regos = self.lineitem_set.filter(event_rego__isnull=False)
        if event_regos.count() > 0:
            summary_str += 'Events\n'
            summary_str += '-----\n'
            for l in event_regos:
                summary_str += '%s: %s - $%.2fAUD\n' % (
                    l.event_rego.event.name,
                    l.event_rego.event_option.name,
                    float(l.event_rego.event_option.cost),
                )
            summary_str += '\n'

        if self.cost > Decimal(0.):
            summary_str += 'TOTAL COST: $%.2fAUD\n' % self.cost
            summary_str += 'All costs are GST-inclusive.\n'

        # Add in any meetings/events which are already paid for, or have
        # zero-cost
        other_meeting_regos = Registration.objects.filter(
            attendee=self.attendee
        ).filter(
            Q(meeting_rego__cost=Decimal(0.)) | Q(is_paid=True)
        )
        other_event_regos = EventRegistration.objects.filter(
            attendee=self.attendee
        ).filter(
            Q(event_option__cost=Decimal(0.)) | Q(is_paid=True)
        )
        if other_meeting_regos.count() > 0 or other_event_regos.count() > 0:
            summary_str += '\nPaid-for/free meetings and events\n'
            summary_str += '-----\n'
            summary_str += 'You are also registered for the following ' \
                           'meetings and events which have already been ' \
                           'paid for, or are free:\n'
            for m in other_meeting_regos:
                summary_str += '%s: %s - $%.2fAUD\n' % (
                    m.meeting.name,
                    m.meeting_rego.name,
                    float(m.meeting_rego.cost)
                )
            for e in other_event_regos:
                summary_str += '%s: %s - $%.2fAUD\n' % (
                    e.event.name,
                    e.event_option.name,
                    float(e.event_option.cost)
                )

        return summary_str

    def generate_summary_html(self):
        summary_str = '<h2>Registration summary</h2>'

        summary_str += '<p>%s<br />' % self.attendee.address_str()
        summary_str += '%s<br />%s</p>' % (
            self.attendee.phone,
            self.attendee.email,
        )

        summary_str += '<p>%s<br />%s<br />%s</p>' % (
            self.attendee.get_academic_level_display(),
            self.attendee.institution,
            self.attendee.membership_pretty()
        )

        # Step through each meeting and add the relevant information
        meeting_regos = self.lineitem_set.filter(meeting_rego__isnull=False)
        if meeting_regos.count() > 0:
            summary_str += '<h3>Meetings</h3>'
            summary_str += '<ul>'
            for l in meeting_regos:
                summary_str += '<li>%s: %s - $%.2fAUD</li>' % (
                    l.meeting_rego.meeting.name,
                    l.meeting_rego.meeting_rego.name,
                    float(l.meeting_rego.meeting_rego.cost),
                )
            summary_str += '</ul>'
        # Step through each event and add the relevant information
        event_regos = self.lineitem_set.filter(event_rego__isnull=False)
        if event_regos.count() > 0:
            summary_str += '<h3>Events</h3>'
            summary_str += '<ul>'
            for l in event_regos:
                summary_str += '<li>%s: %s - $%.2fAUD</li>' % (
                    l.event_rego.event.name,
                    l.event_rego.event_option.name,
                    float(l.event_rego.event_option.cost),
                )
            summary_str += '</ul>'

        if self.cost > Decimal(0.):
            summary_str += '<h3>TOTAL COST: $%.2fAUD</h3>' % self.cost
            summary_str += '<p>All costs are GST-inclusive.</p>'

        # Add in any meetings/events which are already paid for, or have
        # zero-cost
        other_meeting_regos = Registration.objects.filter(
            attendee=self.attendee
        ).filter(
            Q(meeting_rego__cost=Decimal(0.)) | Q(is_paid=True)
        )
        other_event_regos = EventRegistration.objects.filter(
            attendee=self.attendee
        ).filter(
            Q(event_option__cost=Decimal(0.)) | Q(is_paid=True)
        )
        if other_meeting_regos.count() > 0 or other_event_regos.count() > 0:
            summary_str += '<h3>Paid-for/free meetings and events</h3>'
            summary_str += '<p>You are also registered for the following ' \
                           'meetings and events which have already been ' \
                           'paid for, or are free:</p>'
            summary_str += '<ul>'
            for m in other_meeting_regos:
                summary_str += '<li>%s: %s - $%.2fAUD</li>' % (
                    m.meeting.name,
                    m.meeting_rego.name,
                    float(m.meeting_rego.cost)
                )
            for e in other_event_regos:
                summary_str += '<li>%s: %s - $%.2fAUD</li>' % (
                    e.event.name,
                    e.event_option.name,
                    float(e.event_option.cost)
                )
            summary_str += '</ul>'

        return summary_str

    # def send_email_generated(self):
    #     # Send an email to the attendee with their registration details
    #     # This looks broadly like the table
    #     # Form the EmailMessage object
    #     msg_body = 'Thank you for registering for ASA 2018. Your ' \
    #                'registration details are shown below. We will send you the payment' \
    #                'information soon.'
    #
    #     # Hitting the URL again adds another cost - we don't want to do that
    #     # if self.cost > 0:
    #     #     msg_body += '\n\nYou should have been redirected to the ANU ' \
    #     #                 'OneStop system to settle your regisration account. ' \
    #     #                 'If you were not, or you lost the browser window you ' \
    #     #                 'registered in, you can access your account at: %s' % (
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict())
    #     #     )
    #
    #     msg_body += '\n\n %s' % self.generate_summary_string()
    #
    #     msg = django.core.mail.EmailMultiAlternatives(
    #         'ASA2018 - Registration received',
    #         msg_body,
    #         settings.REGISTRATION_EMAIL,
    #         [self.attendee.email, ],
    #     )
    #
    #     # Create the HTML version of the message
    #     msg_body_html = '<html><body>'
    #     msg_body_html += '<p>Thank you for registering for ASA 2018. Your ' \
    #                      'registration details are shown below. We will send  ' \
    #                      'you the payment ' \
    #                      'information soon.</p>'
    #
    #     # Hitting the URL again adds another cost - we don't want to do that
    #     # if self.cost > 0:
    #     #     msg_body_html += '<p>You should have been redirected to the ANU ' \
    #     #                 'OneStop system to settle your regisration account. ' \
    #     #                 'If you were not, or you lost the browser window you ' \
    #     #                 'registered in, you can access your account at: ' \
    #     #                      '<a href="%s">%s</a></p>' % (
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict()),
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict())
    #     #     )
    #
    #     msg_body_html += self.generate_summary_html()
    #     msg_body_html += '</body></html>'
    #
    #     # Attach the HTML version of the email
    #     msg.attach_alternative(
    #         msg_body_html,
    #         "text/html"
    #     )
    #     # Send
    #     msg.send()
    #
    # def send_email_paid(self, summary_str, summary_html):
    #     # Send an email to the attendee with their registration details
    #     # This looks broadly like the table
    #     # Form the EmailMessage object
    #     msg_body = 'Thanks! Your payment for the registration shown below ' \
    #                'has been confirmed by OneStop. See you in July!'
    #
    #     # Hitting the URL again adds another cost - we don't want to do that
    #     # if self.cost > 0:
    #     #     msg_body += '\n\nYou should have been redirected to the ANU ' \
    #     #                 'OneStop system to settle your regisration account. ' \
    #     #                 'If you were not, or you lost the browser window you ' \
    #     #                 'registered in, you can access your account at: %s' % (
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict())
    #     #     )
    #
    #     msg_body += '\n\n %s' % summary_str
    #
    #     msg = django.core.mail.EmailMultiAlternatives(
    #         'ASA2017 - Registration received',
    #         msg_body,
    #         settings.REGISTRATION_EMAIL,
    #         [self.attendee.email, ],
    #     )
    #
    #     # Create the HTML version of the message
    #     msg_body_html = '<html><body>'
    #     msg_body_html += '<p>Thanks! Your payment for the registration ' \
    #                      'shown below ' \
    #                      'has been confirmed by OneStop. See you in July!</p>'
    #
    #     # Hitting the URL again adds another cost - we don't want to do that
    #     # if self.cost > 0:
    #     #     msg_body_html += '<p>You should have been redirected to the ANU ' \
    #     #                 'OneStop system to settle your regisration account. ' \
    #     #                 'If you were not, or you lost the browser window you ' \
    #     #                 'registered in, you can access your account at: ' \
    #     #                      '<a href="%s">%s</a></p>' % (
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict()),
    #     #         settings.ONESTOP_PAYMENT_URL + '?' +
    #     #         urllib.urlencode(self.get_dict())
    #     #     )
    #
    #     msg_body_html += summary_html
    #     msg_body_html += '</body></html>'
    #
    #     # Attach the HTML version of the email
    #     msg.attach_alternative(
    #         msg_body_html,
    #         "text/html"
    #     )
    #     # Send
    #     msg.send()

    def generate_invoice_pdf(self):
        """
        Generate an invoice PDF for this Payment object

        Note that this function will compose the PDF within an io.BytesIO
        buffer object, and return the value of buffer.getvalue(). It is then
        the responsibility of the function caller to do something with this
        output (i.e. write to file, attach to email, output at Django
        HTTP response, etc.).

        Returns
        -------
        buffer_output : ???
            The output PDF, as the output of a virtual file buffer.
        """
        # Start the buffer
        buffer = BytesIO()

        # Initialize the document
        doc = SimpleDocTemplate(buffer)

        # Commence the document 'story'
        story = [Spacer(1, 0.2*inch)]

        p = Paragraph(
            'TAX INVOICE',
            ParagraphStyle('Header-Invoice', fontSize=18)
        )
        story.append(p)
        story.append(Spacer(1, 1 * pica))
        p = Paragraph(
            'ID: {}'.format(self.order_id, ),
            getSampleStyleSheet()['Normal'],
        )
        story.append(p)
        story.append(Spacer(1, 0.5 * inch))

        p = Paragraph(
            '{}<br/>ABN: {}<br/><br/>{}'.format(
                settings.INVOICE_NAME,
                settings.INVOICE_ABN,
                settings.INVOICE_ADDRESS,
            ),
            getSampleStyleSheet()['Normal'],
        )
        story.append(p)
        p = Paragraph(
            '<br/><b>Date:</b> {}'.format(
                timezone.localtime(
                    timezone.now(), timezone.get_current_timezone()).strftime(
                    '%d %b %Y')),
            getSampleStyleSheet()['Normal'],
        )
        story.append(p)

        p = Paragraph(
            '<br/><b>To:</b> {}<br />{}<br />{}'.format(
                strip_accents(self.attendee.full_name()),
                self.attendee.institution,
                self.attendee.address,
            ),
            getSampleStyleSheet()['Normal'],
        )
        story.append(p)
        story.append(Spacer(1, 0.5 * inch))

        # Construct the table of charges
        charge_data = [['Item', 'Total', ]]
        charge_data += [
            [_.get_lineitem_name(), _.get_lineitem_cost()] for _ in
            self.lineitem_set.all()
        ]
        charge_data.append([
            'Total cost (includes GST)', '${:2f}'.format(self.compute_cost()),
        ])
        charge_table = Table(charge_data)
        charge_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONT', (0, -1), (-1, -1), 'Times-Bold'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEABOVE', (0, 1), (-1, 1), 2, colors.black),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBEFORE', (0, 0), (-1, -1), 1, colors.black),
            ('LINEAFTER', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGNMENT', (0, 0), (0, 1), 'LEFT'),
            ('ALIGNMENT', (1, 0), (1, -1), 'RIGHT'),
        ]))
        story.append(charge_table)

        if self.is_paid:
            story.append(Spacer(1, 0.5*inch))
            p = Paragraph(
                'Paid in full at {}'.format(
                    timezone.localtime(self.paid_at,
                                       timezone.get_current_timezone()).strftime(
                        '%d %b %Y %H:%M %Z'
                    )
                ),
                ParagraphStyle('red-emph', textColor='red',
                               alignment=enums.TA_CENTER)
            )
            story.append(p)

        story.append(Spacer(1, 0.5*inch))

        p = Paragraph(
            """
            Invoice generated at {}.<br/>
            This invoice supersedes any previous invoices with the same invoice ID.
            """.format(timezone.localtime(timezone.now(),
                                          timezone.get_current_timezone()).strftime('%d %b %Y %H:%M %Z')),
            ParagraphStyle('footer', alignment=enums.TA_CENTER, fontSize=8))
        story.append(p)

        doc.build(story)

        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    def send_invoice_pdf(self, fail_silently=False):
        eml = django.core.mail.EmailMessage(
            subject='{} - Tax invoice {}'.format(
                settings.GLOBAL_PAGE_TITLE,
                self.order_id,
            ),
            body='Thank you for registering for {}. Please '
                 'find attached your tax invoice.'
                 ''.format(settings.GLOBAL_PAGE_TITLE),
            from_email=settings.REGISTRATION_EMAIL,
            to=[self.attendee.email, ],
            attachments=[
                ('{}-invoice-{}.pdf'.format(
                    settings.GLOBAL_PAGE_TITLE,
                    self.order_id,
                ),
                 self.generate_invoice_pdf(),
                 'application/pdf'),
            ]
        )
        eml.send(fail_silently=fail_silently)

    def __unicode__(self):
        return '%s (%s)' % (self.order_id, self.attendee.full_name(
            capitalize_family=True
        ), )

    def save(self, *args, **kwargs):
        if not self.order_id:
            save_success = False
            while not save_success:
                self.generate_order_id(save=False)
                try:
                    super(Payment, self).save(*args, **kwargs)
                    save_success = True
                except (KeyError, IntegrityError):
                    self.order_id += '1'
        else:
            super(Payment, self).save(*args, **kwargs)
        # Go through and, if paid=True and paid_amount=cost, set all the
        # registrations and event registrations to be paid
        meeting_regos = Registration.objects.filter(lineitem__payment=self)
        # print('%d meeting regos' % len(meeting_regos))
        event_regos = EventRegistration.objects.filter(lineitem__payment=self)
        payment_correct = self.is_paid and (self.paid_amount == self.cost)
        # print('Updating rego paid status')
        for rego in meeting_regos:
            rego.is_paid = payment_correct
            rego.save()
        for rego in event_regos:
            rego.is_paid = payment_correct
            rego.save()

    def delete(self, *args, **kwargs):
        # Set all attached items to unpaid
        meeting_regos = Registration.objects.filter(
            lineitem__payment=self,
            meeting_rego__cost__gt=Decimal(0.),
        )
        # print('%d meeting regos' % len(meeting_regos))
        event_regos = EventRegistration.objects.filter(
            lineitem__payment=self,
            event_option__cost__gt=Decimal(0.),
        )
        # print('Updating rego paid status')
        for rego in meeting_regos:
            rego.is_paid = False
            rego.save()
        for rego in event_regos:
            rego.is_paid = False
            rego.save()
        for l in self.lineitem_set.all():
            l.delete()
        super(Payment, self).delete(*args, **kwargs)


class LineItem(models.Model):
    """
    Records a payment for a single meeting or event registrations
    """
    class Meta:
        ordering = ['attendee', ]
        unique_together = (
            ('attendee', 'meeting_rego',),
            ('attendee', 'event_rego', ),
        )

    # Model fields
    attendee = models.ForeignKey(Attendee, null=False)
    meeting_rego = models.OneToOneField(Registration, null=True, blank=True)
    event_rego = models.OneToOneField(EventRegistration, null=True, blank=True)
    # value = models.DecimalField(max_digits=6, decimal_places=2,
    #                             blank=False, null=False)
    payment = models.ForeignKey(Payment, null=False, default=None)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super(LineItem, self).clean()
        # Make sure that at least one of meeting_rego or event_rego is set
        if self.meeting_rego is None and self.event_rego is None:
            raise ValidationError('Exactly one of meeting_rego '
                                  'or event_rego must be set for a LineItem')
        if self.meeting_rego is not None and self.event_rego is not None:
            raise ValidationError('Only one of meeting_rego '
                                  'or event_rego can be set for a LineItem')
        if self.meeting_rego is not None:
            if not self.attendee == self.meeting_rego.attendee:
                raise ValidationError('All components of LineItem must '
                                      'correspond to the same Attendee')
        else:
            if not self.attendee == self.event_rego.attendee:
                raise ValidationError('All components of LineItem must '
                                      'correspond to the same Attendee')
        # Set the cost to be that of the necessary rego

    def __unicode__(self):
        return '%s, %s, %s' % (
            self.attendee.family_name,
            self.meeting_rego.meeting if self.meeting_rego else self.event_rego.event,
            self.payment,
        )

    def delete(self, *args, **kwargs):
        if self.meeting_rego is not None and \
                self.meeting_rego.cost > Decimal(0.):
            self.meeting_rego.is_paid = False
        elif self.event_rego is not None and \
                self.even_option.cost > Decimal(0.):
            self.event_rego.is_paid = False
        super(LineItem, self).delete(*args, **kwargs)

    def get_lineitem_name(self):
        return '{} - {}'.format(
            self.meeting_rego.meeting if self.meeting_rego else
            self.event_rego.event,
            self.meeting_rego.meeting_rego.name if self.meeting_rego else
            self.event_rego.event_option.name,
        )

    def get_lineitem_cost(self):
        return '${:.2f}'.format(
            self.meeting_rego.meeting_rego.cost if self.meeting_rego else
            self.event_rego.event_option.cost
        )


class DietaryRestriction(models.Model):
    """
    Attached to an EventRegistration object to record any dietary restrictions
    required by the guest(s)
    """
    RESTRICTION_CHOICES = (
        # ('a', 'None'),
        ('v', 'Vegetarian'),
        ('vn', 'Vegan'),
        ('g', 'Gluten-free'),
        ('d', 'Dairy-free'),
        ('s', 'Seafood-free'),
        # ('o', 'Other'),
    )

    class Meta:
        ordering = ('event_rego__attendee', 'event_rego__event', )

    event_rego = models.ForeignKey(EventRegistration, unique=False, null=False)
    restriction = MultiSelectField(blank=True,
                                   choices=RESTRICTION_CHOICES,)
    other_restriction = models.CharField(blank=True, default='',
                                         max_length=200)

    def __unicode__(self):
        return '%s - %s - of %d' % (self.event_rego.event.name,
                                    self.event_rego.attendee.family_name,
                                    DietaryRestriction.objects.filter(
                                        event_rego__attendee=
                                        self.event_rego.attendee,
                                        event_rego__event=self.event_rego.event,
                                    ).count(),
                                    )

    def delete(self, *args, **kwargs):
        print('Watch out! A DietaryRestriction is vanishing!')
        super(DietaryRestriction, self).delete(*args, **kwargs)

    def pretty_print(self):
        """
        Human-readable representation of this DR
        """
        if self.restriction:
            if self.other_restriction:
                return '%s, %s' % (self.get_restriction_display(),
                                   self.other_restriction)
            else:
                return self.get_restriction_display()
        else:
            return self.other_restriction


class Session(models.Model):
    """
    Describes a particular conference session
    """

    class Meta:
        ordering = ('time_start', 'title', 'time_end', )
        unique_together = ('meeting', 'time_start', 'time_end', 'title', )

    # Model fields
    meeting = models.ForeignKey(Meeting, blank=False)
    title = models.CharField(max_length=200, blank=False,
                             help_text='Session title')
    blurb = models.CharField(max_length=50, blank=True,
                             help_text='Short blurb about session contents')
    extended_description = RichTextUploadingField(blank=True,
                                                    help_text="Use this field "
                                                              "if a longer "
                                                              "description is "
                                                              "required, e.g. "
                                                              "for a special "
                                                              "lunch")
    time_start = models.DateTimeField(blank=False)
    time_end = models.DateTimeField(blank=False)
    chair = models.ForeignKey(Attendee, blank=True, null=True)
    location = models.CharField(blank=True, max_length=300,
                                help_text='Address or other simple location '
                                          'of the event (you can add more '
                                          'description, Google Maps etc. in '
                                          'the event description. You can wrap '
                                          'your description in link tags if '
                                          'you do want to link to Google Maps '
                                          'from here.')


    def __unicode__(self):
        return '%s (%s to %s) - %s' % (
            self.title,
            localtime(self.time_start).strftime('%Y-%m-%d %H:%M'),
            localtime(self.time_end).strftime('%Y-%m-%d %H:%M'),
            self.meeting.abbrv,
        )

    def slug(self):
        return slugify(self.title + self.time_start.strftime('%m-%d-%H-%M') +
                       self.time_end.strftime('%m-%d-%H-%M') +
                       self.meeting.abbrv)


class Presentation(models.Model):
    """
    Describes a conference presentation
    """
    class Meta:
        unique_together = (('meeting', 'title', 'presenter', ),
                           ('meeting', 'type', 'id_no', 'media'),
                           )
        ordering = ('time_start', 'time_end', 'id_no', 'presenter', 'title', 'media')

    TYPE_CHOICES = (
        ('t', 'Talk'),
        # ('i', 'Invited talk'),
        ('p', 'Poster'),
    )
    STATUS_CHOICES = (
        ('s', 'Submitted'),
        ('a', 'Accepted'),
        ('d', 'Demoted'),
        ('r', 'Rejected'),
        ('w', 'Withdrawn'),
    )

    MEDIA_CHOICES = (
        ('n', 'No'),
        ('y', 'Yes'),
    )

    # Model fields
    meeting = models.ForeignKey(Meeting, blank=False,
                                help_text='This is the meeting the '
                                          'presentation is submitted for, '
                                          '*not* the assigned meeting - that '
                                          'is read from the linked Session '
                                          'object',)
    title = models.CharField(max_length=400, blank=False,
                             help_text='Presentation title')
    presenter = models.ForeignKey(Attendee, blank=False)
    abstract = RichTextUploadingField(blank=False,
                                        help_text='Abstract - LaTeX allowed?')

    type = models.CharField(max_length=1, choices=TYPE_CHOICES,
                            blank=False, default=TYPE_CHOICES[0][0])

    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])

    id_no = models.IntegerField(blank=True, null=True,
                                help_text="Leave blank to not use ID number. "
                                          "IDs will be displayed as XNNN, "
                                          "where X is the presentation type "
                                          "(e.g. T for talk, P for poster, "
                                          "etc.)")

    #media = models.BooleanField(blank=False, default=False)
    media = models.CharField(max_length=1, choices=MEDIA_CHOICES,
                            blank=False, default=MEDIA_CHOICES[0][0])

    session = models.ForeignKey(Session, blank=True, null=True)

    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)

    submitted = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - %s' % (self.presenter.family_name,
                            self.title[:30],
                            )

    def clean(self):
        if self.session:
            # Check the session and presentation meetings match
            if self.session.meeting != self.meeting:
                raise ValueError("The selected Session is not for this "
                                 "Presentation's meeting")
            # Check that the talk is fully within the session
            if self.time_start and self.time_end:
                if self.time_start < self.session.time_start or \
                                self.time_end > self.session.time_end:
                    raise ValidationError('The start/end times you set for '
                                          'this Presentation are outside the '
                                          'start/end times of its specified '
                                          'session')

    def generate_id(self):
        if self.id_no:
            return '%s%d' % (self.type.upper(), self.id_no)
        return None

    def generate_secret_key(self):
        """
        Generate a 'secret key' to allow one-off changes to presentation
        status
        """
        # The encrypt sequence is:
        # Django secret key as the key
        # Talk title as the first string
        # Presenter full name
        hashed = hmac.new(settings.SECRET_KEY,
                          str(self.pk),
                          hashlib.sha1)
        hashed.update(self.presenter.full_name())
        repl_pattern = re.compile('[\W]+')
        return repl_pattern.sub('',
                                hashed.digest().encode('base64').rstrip('\n'))

    def get_mgmt_url(self):
        from django.core.urlresolvers import reverse
        return reverse('presentation_mgmt', args=[
            int(self.pk),
        ]).replace('http://web/', 'http://asa2018.swin.edu.au/')



class Prize(models.Model):
    """
    Describes a prize awarded at the meeting, potentially with a Presentation
    attached
    """
    class Meta:
        ordering = ['name', 'meeting', ]

    # Model fields
    meeting = models.ForeignKey(Meeting, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False,
                            help_text='Prize name')
    slug = models.SlugField(max_length=100, blank=False, unique=True,
                            help_text='Recommend you use auto-generated '
                                      'slug')
    about = RichTextUploadingField(help_text='About the prize')
    awardee = models.ForeignKey(Attendee, blank=True, null=True,
                                help_text='Leave blank to just advertise the '
                                          'prize - attach an attendee when '
                                          'you want to make the announcement')
    citation = RichTextUploadingField(blank=True,
                                        help_text='Use this field to provide '
                                                  'the award citation, as well '
                                                  'as give some brief info '
                                                  'about the winner')
    talk = models.ForeignKey(Presentation, blank=True, null=True,
                             help_text='Add/attach the prize talk here')

    # Optional information about who the prize is named for
    named_for = models.CharField(max_length=200, blank=True, null=False,
                                 default='', help_text='Full name of honoree')
    honoree_info = RichTextUploadingField(blank=True,
                                            help_text='Info about who the '
                                                      'prize is'
                                                      'named for')
    honoree_pic = models.ImageField(blank=True, null=True,
                                    help_text='Roughly square photo')

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.meeting.abbrv, )

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('prize', args=[
            self.meeting.slug,
            self.slug,
        ])

