from django import forms
from django.forms import ModelForm, formset_factory
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS

from captcha.fields import CaptchaField

from django_countries.widgets import CountrySelectWidget


class AttendeeForm(ModelForm):
    class Meta:
        model = Attendee
        fields = ['family_name', 'given_names', 'email',
                  'institution', 'is_asa_member', 'is_nz_astro',
                  'gender', 'years_since_phd', 'academic_level',
                  'address', 'city', 'state', 'country', 'postcode', 'phone']
        labels = {
            'name_order': _('Order of your names'),
            'is_asa_member': _('Are you a current ASA member?'),
            'is_nz_astro': _('Are you a New Zealand-based astronomer?'),
            'years_since_phd': _('Years since PhD'),
        }
        error_messages = {
            'family_name': {
                'max_length': _('Family names are limited to 50 characters.'),
            },
            'given_names': {
                'max_length': _('Given names are limited to 100 characters.'),
            },
            'email': {
                'unique': _('This email already exists in our registration '
                            'system. '
                            'If you had to abandon a previous attempt to '
                            'register, please contact us so we can reset your '
                            'dormant registration. '
                            'If you believe this is an '
                            'error, please contact us.'),
            },
            'institution': {
                'required': _('You MUST provide your academic institution.'),
                'max_length': _('Please provide a shorter rendering of your '
                                'institution name.'),
            },
            'academic_level': {
                'required': _('Please select an academic level/appointment.'),
            },
            'gender': {
                'required': _("You must select an option. If you do not wish "
                              "to provide this information, select "
                              "'Do not disclose'"),
            },
            'years_since_phd': {
                'required': _("You must select an option. If you do not wish "
                              "to provide this information, select "
                              "'Do not disclose'"),
            }
        }
        # widgets = {
        #     'country': CountrySelectWidget(),
        # }

    # Add in a captcha field
    captcha = CaptchaField(help_text="Having trouble reading the letters? "
                                     "Do your best - the rest of your "
                                     "form data will be preserved if you get "
                                     "this wrong, and in that case you will "
                                     "get a new CAPTCHA.")


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = [
            'meeting_rego',
            'meeting',
            'attendee',
        ]
        widgets = {
            'meeting': forms.HiddenInput(),
            'attendee': forms.HiddenInput(),
            'meeting_rego': forms.RadioSelect()
        }
        labels = {
            'meeting_rego': _("Please select the registration option you'd "
                              "like"),
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'You have already registered for '
                                   'this meeting. To alter your registration, '
                                   'please contact us directly.'
            }
        }
    #
    # meeting = forms.IntegerField(widget=forms.HiddenInput())
    # attendee = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Force the to_python validator for attendee and meeting to send back
        # ints

        now = timezone.now()
        if self.initial:
            attendee = Attendee.objects.get(
                    pk=self.initial.get('attendee'))
            rego_options = RegoOption.objects.filter(
                meeting=int(self.initial.get('meeting')))
        if self.data:
            if self.prefix:
                prefix_str = self.prefix + '-'
            else:
                prefix_str = ''
            attendee = Attendee.objects.get(
                pk=self.data.get(prefix_str + 'attendee'))
            rego_options = RegoOption.objects.filter(
                meeting=int(self.data.get(prefix_str + 'meeting')))
            # else:
            #     raise ValidationError('A RegistrationForm must be initialized with '
            #                           'a Meeting and Attendee object')
        if self.initial or self.data:
            rego_options = rego_options.filter(
                opens__lte=now
            ).filter(
                closes__gte=now
            ).filter(
                available_to__contains=attendee.academic_level
            )
            if not attendee.is_asa_member:
                rego_options = rego_options.filter(
                    asa_only=False
                )
            if not attendee.is_nz_astro:
                rego_options = rego_options.filter(
                    nz_only=False
                )
            rego_options = rego_options.order_by('cost')
            # self.fields['meeting_rego'] = forms.ModelChoiceField(
            #     # queryset=RegoOption.objects.filter(meeting=self.initial['meeting']),
            #     queryset=rego_options,
            #     required=False, label="Please select the registration option you'd "
            #                           "like",
            #     empty_label="Do not register for this meeting",
            #     widget=forms.RadioSelect())
            self.fields['meeting_rego'].queryset = rego_options

        self.fields['meeting_rego'].empty_label = "Do not register for " \
                                                  "this meeting"
        # self.fields['attendee'].queryset = Attendee.objects.filter(
        #     pk=self.initial['attendee'])
        # self.fields['meeting'].queryset = Meeting.objects.filter(
        #     pk=self.initial['meeting'])


class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['meeting', 'title', 'presenter', 'type', 'media', 'abstract']
        widgets = {
            'presenter': forms.HiddenInput(),
        }
        labels = {'media': _('Would you like your abstract considered for media release?')}
        help_texts = {
            'title': _(''),
            'meeting': _('Please select the meeting you are submitting this '
                         'abstract for'),
            'type': _('Abstract type'),
            'abstract': _('LaTeX input is permitted. Grab the handle at the '
                          'bottom-right of the text area to expand it')
        }

    def __init__(self, *args, **kwargs):
        super(PresentationForm, self).__init__(*args, **kwargs)

        # Restrict the meetings queryset
        if self.initial:
            attendee = Attendee.objects.get(
                pk=self.initial.get('presenter')
            )
        if self.data:
            if self.prefix:
                prefix_str = self.prefix + '-'
            else:
                prefix_str = ''
            attendee = Attendee.objects.get(
                pk=self.data.get(prefix_str + 'presenter'))

        active_regos = Registration.objects.filter(attendee=attendee.pk)
        meetings = Meeting.objects.filter(
            accept_abstracts=True
        ).filter(
            id__in=active_regos.values('meeting_id')
        )

        self.fields['meeting'].queryset = meetings
        self.fields['meeting'].empty_label = None


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['attendee', 'event', 'event_option',
                  'extra_comments']
        widgets = {
            'attendee': forms.HiddenInput(),
            'event': forms.HiddenInput(),
            'event_option': forms.RadioSelect(),
        }
        help_texts = {
            'event_option': 'Please choose a registration option for this '
                            'event',
            'extra_comments': 'Please add any extra comments regarding your '
                              'event registration here',
        }
        labels = {
            'event_option': 'Registration option',
            'extra_comments': 'Extra comments',
        }

    def __init__(self, *args, **kwargs):
        super(EventRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['event_option'].empty_label = 'Do not attend'

        # Restrict the event_option queryset
        if self.initial:
            event = Event.objects.get(
                pk=self.initial['event']
            )
        if self.data:
            if self.prefix:
                prefix_str = self.prefix + '-'
            else:
                prefix_str = ''
            event = Event.objects.get(
                pk=self.data[prefix_str + 'event']
            )

        self.fields['event_option'].queryset = EventOption.objects.filter(
            event=event
        )

    def save(self, *args, **kwargs):
        # If the person doesn't want to come to the event, silently fail
        # the save method, otherwise super it
        if not self.cleaned_data['event_option']:
            return
        obj = super(EventRegistrationForm, self).save(*args, **kwargs)
        return obj


class DietaryRestrictionForm(forms.ModelForm):

    class Meta:
        model = DietaryRestriction
        fields = ['restriction', 'other_restriction']
        help_texts = {
            'restriction': 'Please select all which apply.',
            'other_restriction': 'Please list any restrictions not already '
                                 'stated in this text box'
        }
        labels = {
            'restriction': 'Dietary restriction(s)',
            'other_restriction': 'Any other restrictions?',
        }

        def clean(self):
            # Make the form invalid if both restriction and other_restriction
            # are blank
            cleaned_data = super(DietaryRestrictionForm, self).clean()
            # print(self.cleaned_data)
            # print("inside form clean")
            # raise UserWarning('Inside DietaryRestrictionForm clean method')
            if (len(self.cleaned_data.get('restriction')) == 0 and
                        self.cleaned_data.get('other_restriction') == ''):
                raise forms.ValidationError('A valid DietaryRestriction needs '
                                            'a restriction of some kind')


class RequestAbstractEditForm(forms.Form):
    """
    Used to request a link for editing abstracts, based on email
    """

    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(RequestAbstractEditForm, self).clean()
        # Make sure an Attendee with this email exists
        try:
            if 'email' in self.cleaned_data:
                attendee = Attendee.objects.get(email=self.cleaned_data['email'])
            else:
                raise forms.ValidationError("Please provide your email address.")        
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            raise forms.ValidationError("Sorry, we don't have a registration "
                                        "with that email address.")

