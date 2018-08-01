# Basic page views

from django.http import HttpResponse, HttpResponseRedirect, Http404, \
    HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.forms import modelformset_factory
from django.db.models import Q, Count

from django.contrib import messages

from django.conf import settings

from .models import *
from .helpers import *
from .forms import *
import asa18.views

from django.utils import timezone

from decimal import Decimal

import numpy as np
import re
import urllib
import datetime
import hashlib
import hmac

import stripe

from itertools import groupby


def splash(request):
    now = timezone.now()
    meetings = Meeting.objects.all()
    rego_open = determine_rego_open(now)
    latest_news = News.objects.filter(
        pub_date__lte=now
    ).first()
    sponsors = Sponsor.objects.all()
    return render(request, 'asa18/splash.html',
                  {
                      'now': now,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'rego_open': rego_open,
                      'latest_news': latest_news,
                      'sponsors': sponsors,
                  })


def meeting_splash(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    now = timezone.now()
    meetings = Meeting.objects.all()
    rego_open = determine_rego_open(now)
    return render(request, 'asa18/meeting_master.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': rego_open,
                  })


def event(request, eventslug, meeting):
    eventslug = get_object_or_404(Event, slug=eventslug)
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting not in eventslug.meetings.all():
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/event.html',
                  {
                      'event': eventslug,
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })


def event_index(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.event_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/event_index.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'events': meeting.event_set.all(),
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })


def news_index_nomeeting(request):
    return news_index(request, meeting=None)


def news_index(request, meeting=None):
    meetings = Meeting.objects.all()
    if meeting is not None:
        meeting = get_object_or_404(Meeting, slug=meeting)
        news_items = News.objects.filter(meetings__in=[meeting, ]).filter(
            pub_date__lte=timezone.now()
        )
    else:
        news_items = News.objects.filter(
            pub_date__lte=timezone.now()
        )
    return render(request, 'asa18/news_index.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'news_items': news_items,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now())
                  })


def news_nomeeting(request, newsitem):
    return news(request, newsitem, meeting=None)


def news(request, newsitem, meeting=None):
    meetings = Meeting.objects.all()
    news_item = News.objects.get(slug=newsitem)
    if meeting is not None:
        meeting = get_object_or_404(Meeting, slug=meeting)
        if meeting not in news_item.meetings.all() or \
                        news_item.pub_date > timezone.now():
            raise Http404
    return render(request, 'asa18/news.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'news_item': news_item,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now())
                  })


def prize_index(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.prize_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/prize_index.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'prizes': meeting.prize_set.all(),
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })


def prize(request, meeting, prize):
    meeting = get_object_or_404(Meeting, slug=meeting)
    prize = get_object_or_404(Prize, slug=prize)
    if meeting.prize_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/prize.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'prize': prize,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })


def policy(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.policy_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/policy.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'events': meeting.event_set.all(),
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })


def sponsors(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.sponsor_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/sponsors.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'sponsors': meeting.sponsor_set.all(),
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })

def hpc_helpdesk(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.sponsor_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/hpc-helpdesk.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })

def presenter_information(request, meeting):
    meeting = get_object_or_404(Meeting, slug=meeting)
    if meeting.sponsor_set.count() == 0:
        raise Http404
    meetings = Meeting.objects.all()
    return render(request, 'asa18/presenter_info.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                  })

def register_splash(request, success_message=None, error_message=None):
    meetings = Meeting.objects.all()
    # success_message = None
    # error_message = None
    abstract_edit_form = RequestAbstractEditForm()
    now = timezone.now()
    if request.method == 'POST':
        submitted_form = RequestAbstractEditForm(request.POST)
        if submitted_form.is_valid():
            # Note that attendee checking is done as part of form validation,
            # so we can blindly go an get the relevant attendee here without
            # doing error catching
            attendee = Attendee.objects.get(
                email=submitted_form.cleaned_data['email']
            )
            if '_abstract' in request.POST:
                # Count the number of meetings this person is registered for
                # which still have abstracts open for editing
                open_meetings = Meeting.objects.filter(
                    accept_abstracts=True
                ).filter(
                    abstract_date__gte=now
                )
                open_regos = Registration.objects.filter(
                    attendee=attendee
                ).filter(
                    meeting__in=open_meetings
                )
                if open_regos.count() > 0:
                    send_mail('%s - Abstract editing' %
                              settings.GLOBAL_PAGE_TITLE,
                              attendee.generate_abstract_email(reqobj=request),
                              settings.REGISTRATION_EMAIL,
                              [attendee.email, ],
                              fail_silently=False)
                    # Set success message
                    success_message = 'Thanks! You should now receive an email detailing how ' \
                                      'you can access the abstract editing system. ' \
                                      'Please check your spam/junk folders if you ' \
                                      'do not receive this email.'
                else:
                    error_message = 'Sorry, but abstract submission is closed for ' \
                                    'all meetings you are registered for. Please ' \
                                    'contact <a href="mailto:%s">%s</a> if you ' \
                                    'need further assistance.' % (
                        settings.REGISTRATION_EMAIL, settings.REGISTRATION_EMAIL,
                    )
            elif '_checkrego' in request.POST:
                send_mail('%s - Registration check' %
                          settings.GLOBAL_PAGE_TITLE,
                          attendee.generate_check_email(reqobj=request),
                          settings.REGISTRATION_EMAIL,
                          [attendee.email, ],
                          fail_silently=False)
                success_message = 'Thanks! You should now receive an email detailing how ' \
                                  'you can access the registration checking system. ' \
                                  'Please check your spam/junk folders if you ' \
                                  'do not receive this email.'
        else:
            abstract_edit_form = submitted_form
    return render(request, 'asa18/register_splash.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(timezone.now()),
                      'abstract_edit_form': abstract_edit_form,
                      'success_message': success_message,
                      'error_message': error_message,
                  })


def register_person(request):
    meetings = Meeting.objects.all()
    if ~np.any([_.is_rego_open() for _ in meetings]):
        return HttpResponseForbidden('Registration is currently closed.')
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save()
            # Make sure there isn't a latent attendee ID
            _ = request.session.pop('attendee_id', '')
            request.session['attendee_id'] = attendee.id
            request.session.set_expiry(0)  # Session expires on browser close
            return HttpResponseRedirect(reverse(
                asa18.views.register_meetings))
    else:
        form = AttendeeForm()
    return render(request, 'asa18/register_person.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                      'form': form,
                  })


def register_meetings(request):
    meetings = Meeting.objects.all()
    if ~np.any([_.is_rego_open() for _ in meetings]):
        return HttpResponseForbidden('Registration is currently closed.')
    now = timezone.now()
    try:
        attendee = Attendee.objects.get(id=request.session['attendee_id'])
    except KeyError, Attendee.DoesNotExist:
        return HttpResponse('You need to be in the process of registering, '
                            'or altering a registration, to access this page.',
                            status=401)

    meetings_open = {}

    if request.method == 'POST':
        # print request.POST
        if '_abort' in request.POST:
            return register_abort(request)
        meetings_registered_for = 0
        for meeting in meetings:
            if meeting.slug + '-meeting' in request.POST:
                rego_form = RegistrationForm(request.POST, prefix=meeting.slug, )
                meetings_open[meeting] = rego_form
                # print 'Submitted data:'
                # print rego_form.data
                if rego_form.is_valid():
                    if rego_form.cleaned_data['meeting_rego'] is not None:
                        rego_form.save()
                        meetings_registered_for += 1
                # else:
                    # print rego_form.data
        if meetings_registered_for > 0:
            return HttpResponseRedirect(reverse(
                asa18.views.register_presentation
            ))
        else:
            warning_message = "You must register for at least one meeting to " \
                              "proceed! If you do not wish to register for a " \
                              "meeting, please click 'Cancel registration' at " \
                              "the bottom of the page."
    else:
        # For each meeting in the system, we need to go through and identify which
        # registration options are available to the Attendee
        warning_message = None
        for meeting in meetings:
            rego_options = RegoOption.objects.filter(
                meeting=meeting,
                public=True,
            ).filter(
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
            if rego_options.count() > 0:
                option_form = RegistrationForm(initial={
                    'meeting': meeting.id,
                    'attendee': attendee.id,
                    'meeting_rego': None,
                },
                    prefix=meeting.slug)
                # meetings_open[meeting] = rego_options
                meetings_open[meeting] = option_form
        # print meetings_open

    return render(request, 'asa18/register_meetings.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(timezone.now()),
                      'attendee': attendee,
                      'meetings_open': meetings_open,
                      'warning_message': warning_message,
                  })


def register_presentation(request):
    meetings = Meeting.objects.all()
    if ~np.any([_.is_rego_open() for _ in meetings]):
        return HttpResponseForbidden('Registration is currently closed.')
    now = timezone.now()
    try:
        attendee = Attendee.objects.get(id=request.session['attendee_id'])
    except KeyError, Attendee.DoesNotExist:
        return HttpResponse('You need to be in the process of registering, '
                            'or altering a registration, to access this page.',
                            status=401)
    success_message = None

    if request.method == 'POST':
        if '_abort' in request.POST:
            return register_abort(request)
        form = PresentationForm(request.POST)
        if form.is_valid():
            form.save()
            if '_add_another' in request.POST:
                success_message = 'Abstract "%s" submitted' % (
                    form.cleaned_data['title'],
                )
                form = PresentationForm(initial={
                    'presenter': attendee.id,
                })
            else:
                return HttpResponseRedirect(reverse(
                    asa18.views.register_events
                ))
    else:
        form = PresentationForm(initial={
            'presenter': attendee.id,
        })

    # Make sure the attendee is registered for a meeting which accepts
    # abstracts
    regos = Registration.objects.filter(
        attendee=attendee.pk
    ).filter(
        meeting__accept_abstracts=True
    ).filter(
        Q(meeting__abstract_date__gte=now) |
        Q(meeting__abstract_date__isnull=True)
    )
    # Push user along the registration chain if not the case
    if regos.count() == 0:
        return HttpResponseRedirect(reverse(
            asa18.views.register_events
        ))

    # Get this user's already-submitted abstracts
    abstracts_submitted = Presentation.objects.filter(
        presenter_id=request.session['attendee_id']
    )

    return render(request, 'asa18/register_presentation.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(
                          timezone.now()),
                      'attendee': attendee,
                      'form': form,
                      'success_message': success_message,
                      'abstracts_submitted': abstracts_submitted,
                  })


def register_events(request):
    meetings = Meeting.objects.all()
    if ~np.any([_.is_rego_open() for _ in meetings]):
        return HttpResponseForbidden('Registration is currently closed.')
    now = timezone.now()
    try:
        attendee = Attendee.objects.get(id=request.session['attendee_id'])
    except KeyError, Attendee.DoesNotExist:
        return HttpResponse('You need to be in the process of registering, '
                            'or altering a registration, to access this page.',
                            status=401)
    success_message = None

    # Only show events which need rego
    rego_events_opts = EventOption.objects.all()
    full_event_set = Event.objects.filter(
        Q(eventoption__in=rego_events_opts)
    )
    event_dict = {}
    event_form_valid = {}
    dietary_formset_dict = {}

    DietaryRestrictionFormset = modelformset_factory(
                    DietaryRestriction,
                    form=DietaryRestrictionForm,
                    extra=4,
                    # fields=['restriction', 'other_restriction', ]
                )

    if request.method == 'POST':
        if '_abort' in request.POST:
            return register_abort(request)
        for e in full_event_set:
            if e.slug + '-event' in request.POST:
                event_dict[e] = EventRegistrationForm(
                    request.POST, prefix=e.slug)
                if event_dict[e].data.get(
                                e.slug + '-event_option') and \
                                event_dict[e].data.get(
                                            e.slug + '-event_option') != '':

                    event_form_valid[e] = event_dict[e].is_valid()

                    if e.dietary_required:
                        dietary_formset_dict[e] = DietaryRestrictionFormset(
                            request.POST,
                            prefix=e.slug+'diet',
                        )

        if np.all(event_form_valid.values()):
            for valid_event in event_form_valid.keys():
                # print(valid_event)
                rego_opt = event_dict.get(valid_event).save()
                # print 'dietary formset dict looks like:'
                # print dietary_formset_dict
                # print( dietary_formset_dict.get(valid_event) )
                if dietary_formset_dict.get(valid_event) is not None and \
                        valid_event.dietary_required:
                    # Only save as many forms as there are guests
                    for form in dietary_formset_dict.get(valid_event):
                        if form.has_changed() and form.is_valid():
                        # if form.is_valid() and form.cleaned_data != {}:
                        #     print(form.cleaned_data)
                            obj = form.save(commit=False)
                            obj.id = None
                            obj.event_rego = rego_opt
                            obj.save()
            return HttpResponseRedirect(reverse(
                asa18.views.register_confirm
            ))
    else:
        # Restrict the event set to those events available based on
        # the attendee responses
        this_attendee_meetings = Meeting.objects.filter(
            registration__attendee=attendee
        )
        event_set = full_event_set.filter(
            meetings__in=this_attendee_meetings
        )
        if event_set.count() == 0:
            return HttpResponseRedirect(reverse(
                asa18.views.register_confirm
            ))

        for event in event_set:
            event_dict[event] = EventRegistrationForm(
                prefix=event.slug,
                initial={
                    'attendee': attendee.pk,
                    'event': event.pk,
                })
            if event.dietary_required:
                dietary_formset_dict[event] = DietaryRestrictionFormset(
                    prefix=event.slug+'diet',
                    queryset=DietaryRestriction.objects.none(),
                )

    return render(request, 'asa18/register_events.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(
                          timezone.now()),
                      'attendee': attendee,
                      'event_dict': event_dict,
                      'dietary_formset_dict': dietary_formset_dict,
                      'success_message': success_message,
                  })


def register_confirm(request):
    meetings = Meeting.objects.all()
    if ~np.any([_.is_rego_open() for _ in meetings]):
        return HttpResponseForbidden('Registration is currently closed.')
    now = timezone.now()
    if request.session.get('attendee_checkrego_id'):
        request.session['attendee_id'] = request.session.get(
            'attendee_checkrego_id')
        _ = request.session.pop('attendee_checkrego_id')
        coming_from_regocheck = True
    else:
        coming_from_regocheck = False
    try:
        attendee = Attendee.objects.get(id=request.session['attendee_id'])
    except (KeyError, Attendee.DoesNotExist):
        return HttpResponse('You need to be in the process of registering, '
                            'or altering a registration, to access this page.',
                            status=401)
    success_message = None

    # Let's get all the meeting and event registrations this person
    # currently has attached to them
    # Note we should only retrieve those which are not paid for
    regos_meetings = Registration.objects.filter(
        attendee=attendee,
        # lineitem__exact=None,
    )
    regos_events = EventRegistration.objects.filter(
        attendee=attendee,
        # lineitem__exact=None,
    )
    presentations = {}
    for rego in regos_meetings:
        if Presentation.objects.filter(
            presenter=attendee
        ).filter(
            meeting=rego.meeting
        ).count() > 0:
            presentations[rego] = Presentation.objects.filter(
                presenter=attendee
            ).filter(
                meeting=rego.meeting
            )
    # presentations = Presentation.objects.filter(presenter=attendee)

    cost = Decimal(0.)
    for m in regos_meetings:
        cost += m.meeting_rego.cost if not m.is_paid else Decimal(0.)
    for e in regos_events:
        cost += e.event_option.cost if not e.is_paid else Decimal(0.)

    if request.POST:
        if '_abort' in request.POST:
            return register_abort(request)

        if '_personal' in request.POST:
            # Remove the attendee from the session
            a_id = request.session.pop('attendee_id')
            # Delete the attendee
            Attendee.objects.get(id=a_id).delete()
            # Send the user back to register_person
            return HttpResponseRedirect(reverse(
                asa18.views.register_person))

        if '_meeting' in request.POST:
            pass
            # Remove all meeting AND event regos, return to there
            EventRegistration.objects.filter(
                attendee_id=request.session['attendee_id']).delete()
            Registration.objects.filter(
                attendee_id=request.session['attendee_id']).delete()
            return HttpResponseRedirect(reverse(
                asa18.views.register_meetings))

        if '_event' in request.POST:
            EventRegistration.objects.filter(
                attendee_id=request.session['attendee_id']).delete()
            return HttpResponseRedirect(reverse(
                asa18.views.register_events))
            # Remove all events regos, return to there

        # The only remaining POST options are now '_confirm' (which is
        # confirm, but not pay yet), '_invoice' (which doesn't do anything
        # money wise, but emails an invoice) or pay (which doesn't come
        # with a special option name). In any case, we need to eliminate the
        # 'free' options, and construct the payment object

        if cost > Decimal(0.) or '_invoice' in request.POST:
            # Initialize a new Payment object for this transaction
            if Payment.objects.filter(attendee=attendee,
                                      is_paid=False).count() > 0:
                payment_obj = Payment.objects.filter(
                    attendee=attendee, is_paid=False).order_by('-created')[0]
            else:
                payment_obj = Payment(attendee=attendee)
                payment_obj.created = timezone.now()
                # Order ID is now auto-computed on payment obj save
                payment_obj.save()
            for m in regos_meetings:
                if m.meeting_rego.cost > Decimal(0.) and not m.is_paid:
                    # Create line item
                    try:
                        l = LineItem(
                            attendee=attendee,
                            meeting_rego=m,
                            payment=payment_obj,
                        )
                        l.save()
                    except IntegrityError:
                        pass
                else:
                    # Set paid to True and save
                    # No further action required for this rego
                    m.is_paid = True
                    m.save()
            for e in regos_events:
                if e.event_option.cost > Decimal(0.) and not e.is_paid:
                    # Create line item
                    try:
                        l = LineItem(
                            attendee=attendee,
                            event_rego=e,
                            payment=payment_obj,
                        )
                        l.save()
                    except IntegrityError:
                        pass
                else:
                    # Set paid to True and save
                    # No further action required for this rego
                    e.is_paid = True
                    e.save()

            # Collapse any other existing un-settled Payment objects into
            # this new one
            # Note we can do this because we've retrived ALL the registration
            # options attached to this person, not just the ones from the
            # current session
            # Don't blank out the new Payment!
            other_payments = Payment.objects.filter(
                attendee=attendee,
                is_paid=False,
            ).exclude(
                order_id=payment_obj.order_id,
            )
            subsumed_payments = []
            for p in other_payments:
                for l in p.lineitem_set.all():
                    l.payment = payment_obj
                    l.save()
                subsumed_payments.append(p.order_id)
                p.delete()
            if len(subsumed_payments) > 0:
                eml = EmailMessage(
                    subject="{} - cancelled invoices".format(
                        settings.GLOBAL_PAGE_TITLE,
                    ),
                    body='Please be aware that the following unpaid invoices '
                         'have been cancelled: \n\n{}\n\nUnpaid invoices from '
                         'these '
                         'items now appear on invoice {}.'.format(
                        '/n'.join(subsumed_payments),
                        payment_obj.order_id
                    ),
                    from_email=settings.REGISTRATION_EMAIL,
                    to=[attendee.email, ],
                )
                eml.send(fail_silently=False)

            # Compute the payment cost and store it
            payment_obj.cost = payment_obj.compute_cost()
            payment_obj.save()

            if '_confirm' in request.POST:
                # Pop the user, send elsewhere with appropriate message
                payment_obj.send_invoice_pdf(fail_silently=False)
                _ = request.session.pop('attendee_id')
                success_message = "Thanks! Your registration has now been " \
                                  "confirmed. Please use the 'Check " \
                                  "Registration' functionality below to pay " \
                                  "for your registration at a later date."
                messages.success(request, success_message)
                return HttpResponseRedirect(reverse(
                    asa18.views.register_splash))

            elif '_invoice' in request.POST:
                # Send the user back to where they just were with a success
                # message
                # Get any other existing payment objects
                payment_objs = Payment.objects.filter(
                    attendee=payment_obj.attendee
                ).exclude(
                    order_id=payment_obj.order_id
                )
                for payment in payment_objs:
                    payment.send_invoice_pdf(fail_silently=False)
                if payment_obj.cost == Decimal(0.):
                    payment_obj.delete()
                else:
                    payment_obj.send_invoice_pdf(fail_silently=False)
                success_message = "An up-to-date invoice has been sent to " \
                                  "your listed email address."
                messages.success(request, success_message)
                # Use a re-direct to a POST-less version of whichever page
                # sent this request
                if coming_from_regocheck:
                    get_params = urllib.urlencode({
                        'key': attendee.generate_abstract_key(
                            dt=timezone.now()
                        ),
                        'email': attendee.email,
                    })
                    return HttpResponseRedirect('%s?%s' % (
                        reverse('check_rego'), get_params,
                    ))
                else:
                    return HttpResponseRedirect(reverse('register_confirm'))

            else:
                # Do Stripe things to authenticate payment
                # Get the stripe token
                print('Attempting Stripe auth')
                stripe_token = request.POST.get('stripeToken', '')
                # Actually perform the charge
                payment_error = False
                try:
                    print('Attempting to charge')
                    charge = stripe.Charge.create(
                        capture=True,
                        amount=int(payment_obj.cost * 100),
                        currency='aud',
                        description='ASA meeting registration',
                        source=stripe_token,
                        statement_descriptor=
                        settings.STRIPE_STATEMENT_DESCRIPTOR,
                        metadata={
                            'attendee': payment_obj.attendee.id,
                            'name': payment_obj.attendee.full_name(),
                            'asa_invoice_id': payment_obj.order_id,
                        }
                    )
                    print('Charge created')
                    # Payment has been successful - set flags as such
                    payment_obj.is_paid = True
                    payment_obj.paid_at = timezone.now()
                    payment_obj.receipt_no = charge.id
                    payment_obj.paid_amount = Decimal(charge.amount / 100.)
                    payment_obj.invoice_no = charge.invoice if charge.invoice is not None else ''
                    payment_obj.save()
                    # Update the attached LineItem objects
                    for l in LineItem.objects.filter(payment=payment_obj):
                        if l.meeting_rego is not None:
                            l.meeting_rego.is_paid = True
                            l.meeting_rego.save()
                        elif l.event_rego is not None:
                            l.event_rego.is_paid = True
                            l.event_rego.save()

                    print('Internal payment processing complete!')

                    payment_obj.send_invoice_pdf(fail_silently=False)

                    success_message = 'Thanks! Your registration is now ' \
                                      'confirmed and paid for.'
                    messages.success(request, success_message)
                    return HttpResponseRedirect('/')

                except stripe.error.CardError as e:
                    payment_error = True
                    body = e.json_body
                    err = body.get('error', {})
                    print('CARD ERROR')
                    print('Status is: {}'.format(e.http_status))
                    print('Type is: {}'.format(err.get('type')))
                    print('Code is: {}'.format(err.get('code')))
                    print('Param is: {}'.format(err.get('param')))
                    print('Message is: {}'.format(err.get('message')))
                    error_message = 'Your card payment has been declined. ' \
                                    'Please try again, or check with your ' \
                                    'card provider if this is a recurring ' \
                                    'issue.'
                    messages.error(request, error_message)
                except stripe.error.RateLimitError as e:
                    payment_error = True
                    error_message = 'A high level of activity is swamping ' \
                                    'our payment gateway at this time. ' \
                                    'Please wait a minute or two and try ' \
                                    'again.'
                    messages.error(request, error_message)
                except (stripe.error.InvalidRequestError,
                        stripe.error.AuthenticationError,
                        stripe.error.APIConnectionError,
                        stripe.error.StripeError) as e:
                    payment_error = True
                    print(e)
                    error_message = 'There is presently an issue with our ' \
                                    'Stripe payment submission system. ' \
                                    'Please confirm your registration ' \
                                    'without paying below; we will notify ' \
                                    'you when the payment gateway has been ' \
                                    'restored.'
                    messages.error(request, error_message)
                except Exception as e:
                    payment_error = True
                    print(e)
                    error_message = 'Oops, something has gone wrong. Please ' \
                                    'confirm your registration without ' \
                                    'payment below, and contact us to let us ' \
                                    'know what happened.'
                    messages.error(request, error_message)

                if payment_error and coming_from_regocheck:
                    get_params = urllib.urlencode({
                        'key': attendee.generate_abstract_key(
                            dt=timezone.now()
                        ),
                        'email': attendee.email,
                    })
                    return HttpResponseRedirect('%s?%s' % (
                        reverse('check_rego'), get_params,
                    ))

        else:
            # Mark all regos as paid for
            for m in regos_meetings:
                m.is_paid = True
                m.save()
            for e in regos_events:
                e.is_paid = True
                e.save()
            _ = request.session.pop('attendee_id')
            success_message = 'Thanks! Your registration is now ' \
                              'confirmed. No payment is required.'
            messages.success(request, success_message)
            return HttpResponseRedirect('/')

    return render(request, 'asa18/register_confirm.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(
                          timezone.now()),
                      'attendee': attendee,
                      'regos_meetings': regos_meetings,
                      'regos_events': regos_events,
                      'presentations': presentations,
                      'success_message': success_message,
                      'total_cost': cost,
                      'total_cost_cents': int(cost * 100),
                      'stripe_key_public': settings.STRIPE_KEY_PUBLISHABLE,
                  })

def register_abstract_receive(request):
    meetings = Meeting.objects.all()
    now = timezone.now()
    return render(request, 'asa18/register_abstract_receive.html', {
        'banner': get_banner(),
        'meetings': meetings,
        'now': now,
    })

def test404(request):
    meetings = Meeting.objects.all()
    return render(request, 'asa18/404.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(
                          timezone.now()),
                  })


def test500(request):
    meetings = Meeting.objects.all()
    return render(request, 'asa18/500.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(
                          timezone.now()),
                  })


# def confirm_payment(request):
#     if request.GET:
#         # Do Payment processing on our end - throw a BadRequest is everything
#         # doesn't match what we sent to OneStop ourselves
#         # Fetch the relevant payment object
#         try:
#             payobj = Payment.objects.get(order_id=request.GET.get('OrderID'))
#         except Payment.DoesNotExist:
#             print('confirm_payment: Mismatched Order ID')
#             return HttpResponseBadRequest('No record of payment %s' %
#                                           request.GET.get('OrderID'))
#
#         # Compute the secret hash that should have been returned
#         # query_str = request.META.get['QUERY_STRING']
#         # query_str = query_str.split('HASH')[0]  # Chop off the hash
#         # query_str += settings.ONESTOP_SECRET_HASH
#         # # Or, should is be the query string I'd have sent?
#         # query_str = urllib.urlencode(payobj.get_params)
#         # # Stand up an MD5 hash table
#         # h = hmac.new(settings.ONESTOP_SECRET_HASH_KEY,
#         #              query_str,
#         #              hashlib.md5)
#         # # print hash_code
#         # if h.hexdigest() != request.GET.get('HASH'):
#         #     print('confirm_payment: Invalid HASH')
#         #     return HttpResponseBadRequest('Invalid HASH')
#
#         # Verify that the email, store_id, GLCode, payment amount and phone
#         # all match
#         # We won't match on description or name, I'm concerned those may get
#         # mangled when being passed around by GET/inside OneStop
#         tests = []
#         # tests.append(request.GET['Email'] == payobj.attendee.email)
#         # tests.append(request.GET['Phone'] == payobj.attendee.phone)
#         tests.append(request.GET.get('StoreID') == settings.ONESTOP_STOREID)
#         # tests.append(request.GET['GLCode'] == settings.ONESTOP_GLCODE)
#         tests.append(request.GET.get('TranStatus') == 'PG_SUCCESS')
#         tests.append(Decimal(request.GET.get('TotAmt')) == payobj.cost)
#         if not np.all(tests):
#             print('confirm_payment: Failed comparison tests')
#             return HttpResponseBadRequest('Returned information does not '
#                                           'match records for payment %s' %
#                                           request.GET.get('OrderID'))
#         # OK, everything matches, so let's confirm the payment within our
#         # system
#         # Grab the Payment summaries now before we change stuff, so we
#         # can include them in the email
#         summary_str = payobj.generate_summary_string()
#         summary_html = payobj.generate_summary_html()
#         # Modify the Payment object
#         payobj.is_paid = True
#         payobj.paid_at = timezone.now()
#         payobj.invoice_no = request.GET.get('InvoiceNo', 'WARNINGNOTKNOWN')
#         payobj.receipt_no = request.GET.get('ReceiptNo', 'WARNINGNOTKNOWN')
#         payobj.paid_amount = Decimal(request.GET.get('TotAmt', 0.))
#         payobj.save()
#         # Update the attached LineItem objects
#         for l in LineItem.objects.filter(payment=payobj):
#             if l.meeting_rego is not None:
#                 l.meeting_rego.is_paid = True
#                 l.meeting_rego.save()
#             elif l.event_rego is not None:
#                 l.event_rego.is_paid = True
#                 l.event_rego.save()
#
#         payobj.send_email_paid(summary_str, summary_html)
#         return HttpResponse('Payment successfully processed by '
#                             'asa2017.anu.edu.au')
#     else:
#         print('confirm_payment: no GET detected')
#         return HttpResponseBadRequest('Must supply this page with GET params')


def register_abort(request):
    # if request.POST:
    try:
        a_id = Attendee.objects.get(id=request.session['attendee_id'])
    except KeyError, Attendee.DoesNotExist:
        return HttpResponse('You need to be in the process of registering, '
                            'or altering a registration, to access this '
                            'page.',
                            status=401)
    # Delete any registrations unattached to a LineItem which are
    # assigned to this attendee
    Registration.objects.filter(
        attendee=a_id
    ).filter(
        lineitem__isnull=True
    ).delete()
    EventRegistration.objects.filter(
        attendee=a_id
    ).filter(
        lineitem__isnull=True
    ).delete()
    # If the user has no registrations left attached to them, they can
    # be deleted from the system
    if Registration.objects.filter(
        attendee=a_id
    ).count() == 0 and EventRegistration.objects.filter(
        attendee=a_id
    ).count() == 0:
        a_id.delete()
    # End the registration session
    _ = request.session.pop('attendee_id')
    # Send the person back to the home page
    return HttpResponseRedirect('/')


def edit_abstracts(request, id=None):
    submit_target = None
    editing = False

    meetings = Meeting.objects.all()
    now = timezone.now()

    if request.method == 'GET' and len(request.GET) > 0:
        # This occurs at first login
        try:
            attendee = Attendee.objects.get(email__iexact=request.GET.get('email'))
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            return HttpResponseBadRequest('No conference attendee with this '
                                          'email exists!')
        test_key = attendee.generate_abstract_key()
        if test_key == request.GET.get('key'):
            request.session['attendee_abstract_id'] = attendee.pk
            form = PresentationForm(initial={'presenter': attendee.pk})
        else:
            return HttpResponseForbidden('The URL you have accessed is '
                                         'invalid. '
                                         'Please request a new URL for editing '
                                         'your abstracts.')
    elif request.method == 'POST':
        form = None

        # Check the session attendee value
        try:
            attendee = Attendee.objects.get(
                pk=request.session.get('attendee_abstract_id')
            )
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            return HttpResponseForbidden('Your session may have expired. '
                                         'Please request a new URL from '
                                         'the registration website.')
        # Action the request based on whether it's an add, edit or remove
        if '_add_another' in request.POST:
            if id:
                instance = get_object_or_404(Presentation, id=id)
            else:
                instance = None
            form = PresentationForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                form = None
        elif '_exit' in request.POST:
            # Remove the attendee in session
            _ = request.session.pop('attendee_abstract_id')
            return HttpResponseRedirect(reverse(
                asa18.views.register_splash))
        elif np.any([_.startswith('_alter') for _ in request.POST]):
            # Get the alteration string
            alt_string = [_ for _ in request.POST if _.startswith('_alter')][0]
            # Get the PK of the presentation to edit
            pres_pk = alt_string.split('_')[-1]
            try:
                pres_to_alt = Presentation.objects.get(pk=pres_pk)
            except Presentation.DoesNotExist:
                return HttpResponseBadRequest('The presentation you wish to '
                                              'alter does not exist!')
            form = PresentationForm(instance=pres_to_alt)
            submit_target = reverse(asa18.views.edit_abstracts,
                                    kwargs={'id': pres_pk})
            editing = True
        elif np.any([_.startswith('_delete') for _ in request.POST]):
            # Get the alteration string
            del_string = [_ for _ in request.POST if _.startswith('_delete')][0]
            # Get the PK of the presentation to edit
            pres_pk = del_string.split('_')[-1]
            try:
                Presentation.objects.get(pk=pres_pk).delete()
            except Presentation.DoesNotExist:
                return HttpResponseBadRequest('The presentation you wish to '
                                              'delete does not exist!')
        # Generate a form to return if necessary
        if form is None:
            form = PresentationForm(initial={'presenter': attendee.pk})
    else:
        # This may occur if the user hits the raw abstract edit URL for some
        # reason
        # Should check the session attendee value, then give a blank form
        try:
            attendee = Attendee.objects.get(
                pk=request.session.get('attendee_abstract_id')
            )
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            return HttpResponseForbidden('You must have requested a special '
                                         'URL to access this page.')
        form = PresentationForm(initial={'presenter': attendee.pk})

    # Get the attendees existing presentations
    abstracts_submitted = Presentation.objects.filter(presenter=attendee)

    # If not set by the update algorithm, get the submit target
    if submit_target is None:
        submit_target = reverse(asa18.views.edit_abstracts)

    # Get the remaining required information
    remain = datetime.datetime.combine(now.date() +
                                       datetime.timedelta(
                                           1.
                                       ),
                                       datetime.time(
                                           0, 0, 0,
                                           tzinfo=
                                           timezone.get_current_timezone())
                                       ) - now
    remain_hrs = int(remain.total_seconds() / 3600)
    remain_min = int((remain.total_seconds() % 3600.) / 60.)

    return render(request, 'asa18/presentation_edit.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'remain_hrs': remain_hrs,
                      'remain_min': remain_min,
                      'rego_open': determine_rego_open(
                          timezone.now()),
                      'attendee': attendee,
                      'form': form,
                      'abstracts_submitted': abstracts_submitted,
                      'submit_target': submit_target,
                      'editing': editing,
                  })


def check_rego(request):
    attendee = None
    meetings = Meeting.objects.all()
    success_message = None
    if request.method == 'GET' and len(request.GET) > 0:
        # This occurs at first login
        try:
            attendee = Attendee.objects.get(
                email__iexact=request.GET.get('email'))
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            return HttpResponseBadRequest('No conference attendee with this '
                                          'email exists!')
        test_key = attendee.generate_abstract_key()
        if test_key == request.GET.get('key'):
            request.session['attendee_checkrego_id'] = attendee.pk
        else:
            return HttpResponseForbidden('The URL you have accessed is '
                                         'invalid. '
                                         'Please request a new URL for '
                                         'checking your registration.')

    if attendee is None:
        try:
            attendee = Attendee.objects.get(pk=request.session.get(
                'attendee_checkrego_id'))
        except Attendee.DoesNotExist, Attendee.MultipleObjectsReturned:
            return HttpResponseForbidden('You need to have requested '
                                         'a special URL to view this page.')

    # Fetch the attendee registration info
    # Let's get all the meeting and event registrations this person
    # currently has attached to them
    # Note we should only retrieve those which are not paid for
    regos_meetings = Registration.objects.filter(
        attendee=attendee,
        # lineitem__exact=None,
    )
    regos_events = EventRegistration.objects.filter(
        attendee=attendee,
        # lineitem__exact=None,
    )
    presentations = {}
    for rego in regos_meetings:
        if Presentation.objects.filter(
                presenter=attendee
        ).filter(
            meeting=rego.meeting
        ).count() > 0:
            presentations[rego] = Presentation.objects.filter(
                presenter=attendee
            ).filter(
                meeting=rego.meeting
            )

    cost = Decimal(0.)
    for m in regos_meetings:
        cost += m.meeting_rego.cost if not m.is_paid else Decimal(0.)
    for e in regos_events:
        cost += e.event_option.cost if not e.is_paid else Decimal(0.)

    return render(request, 'asa18/register_check.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': timezone.now(),
                      'rego_open': determine_rego_open(
                          timezone.now()),
                      'attendee': attendee,
                      'regos_meetings': regos_meetings,
                      'regos_events': regos_events,
                      'presentations': presentations,
                      'success_message': success_message,
                      'total_cost': cost,
                      'total_cost_cents': int(cost*100),
                      'stripe_key_public': settings.STRIPE_KEY_PUBLISHABLE,
                  })


def presentation_mgmt(request, pk):
    """
    Super-view for some basic presentation actions. Currently allowed actions
    are:
    convert-to-poster: Convert a rejected talk to a poster
    withdraw-rejected: Withdraw a rejected presentation
    """
    pres = get_object_or_404(Presentation, pk=pk)

    if request.method == 'GET' and len(request.GET) > 0:
        testkey = pres.generate_secret_key()
        if testkey != request.GET.get('key'):
            return HttpResponseBadRequest('Invalid access key')
    else:
        return HttpResponseBadRequest('Invalid request')

    action = request.GET.get('action').lower()
    if action == 'convert-to-poster':
        if pres.type != 't':
            return_message = 'Your %s "%s" is not a talk, so cannot be ' \
                             'converted to a poster automatically. If you ' \
                             'would like to change your presentation type, ' \
                             'please contact us directly.' % (
                pres.get_type_display().lower(),
                pres.title,
            )
            message_type = 'warning'
        elif pres.status != 'r':
            return_message = 'Your talk "%s" has not been rejected ' \
                             '(current status: %s), so we ' \
                             'have not automatically converted it to a ' \
                             'poster. If you would like us to do so, please ' \
                             'contact us directly.' % (
                pres.title,
                pres.get_status_display().lower(),
            )
            message_type = 'warning'
        else:
            # Actually do stuff
            pres.type = 'p'
            pres.status = 'a'
            pres.save()
            return_message = 'Your talk "%s" has been successfully converted ' \
                             'to a poster and accepted for presentation.' % (
                pres.title,
            )
            message_type = 'success'
    elif action == 'withdraw-rejected':
        if pres.status != 'r':
            return_message = 'Your %s "%s" has not been rejected ' \
                             '(current status: %s), so we ' \
                             'have not automatically withdrawn it for you. ' \
                             'If you wish for us to do so (or otherwise ' \
                             'change its status), please contact ' \
                             'us directly.' % (
                                 pres.get_type_display().lower(),
                                 pres.title,
                                 pres.get_status_display().lower(),
                             )
            message_type = 'warning'
        else:
            pres.status = 'w'
            pres.save()
            return_message = 'Your %s "%s" has been successfully withdrawn.' % (
                                 pres.get_type_display(),
                                 pres.title,
                             )
            message_type = 'success'
    else:
        return HttpResponseBadRequest('Unknown action type')

    meetings = Meeting.objects.all()
    now = timezone.now()

    return render(request, 'asa18/presentation_mgmt.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(now),
                      'return_message': return_message,
                      'message_type': message_type,
                  })


def rego_summary(request):
    """
    Show an admin-level registration summary
    """
    # Check that the superuser is active
    if not request.user.is_superuser:
        return HttpResponseForbidden('You must be logged in - go to the admin '
                                     'site, log in there, then return to this '
                                     'page.')

    meetings = Meeting.objects.all()
    now = timezone.now()
    rego_info = {}
    event_info = {}
    dr_info = {}

    for meeting in meetings:
        this_meet_info = {}
        this_meet_info['Attendees'] = Registration.objects.filter(
            meeting=meeting
        ).count()
        this_meet_info['Talk abstracts'] = Presentation.objects.filter(
            meeting=meeting
        ).filter(
            type='t'
        ).count()
        this_meet_info['Poster abstracts'] = Presentation.objects.filter(
            meeting=meeting
        ).filter(
            type='p'
        ).count()
        rego_info[meeting.slug] = this_meet_info

        this_meet_events = {}
        this_meet_drs = {}
        for e in Event.objects.filter(meetings__in=[meeting, ]).annotate(
            option_count=Count('eventoption')
        ).filter(
            option_count__gte=1
        ):
            extra_guests = EventRegistration.objects.filter(
                event=e
            ).aggregate(sum_extra=Sum('event_option__extra_guests'))[
                'sum_extra'
            ]
            if extra_guests is None:
                extra_guests = 0
            this_meet_events[e.name] = EventRegistration.objects.filter(
                event=e
            ).count() + extra_guests
            # Get any dietary restrictions attached to this event, and
            # aggregate them together
            drs = DietaryRestriction.objects.filter(
                event_rego__event=e
            ).order_by('restriction', 'other_restriction')
            # print('There are %d DRs attached to %s' % (drs.count(),
            #                                            e.name, ))
            attempted_count = {k: len(list(v)) for k, v in
                               groupby(drs,
                                       key=lambda x: x.pretty_print())}
            # print(attempted_count)
            this_meet_drs[e] = attempted_count

        event_info[meeting.slug] = this_meet_events
        dr_info[meeting.slug] = this_meet_drs

    return render(request, 'asa18/rego_summary.html',
                  {
                      'meeting': None,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(now),
                      'rego_info': rego_info,
                      'event_info': event_info,
                      'dr_info': dr_info,
                  })


def meeting_participants(request, meeting):
    """
    Display a summary of the meeting participants, including the
    proportions of various attendee types
    """

    meeting = get_object_or_404(Meeting, slug=meeting)
    meetings = Meeting.objects.all()

    meeting_loc = meeting.meetings_loc.all()
    meeting_soc = meeting.meetings_soc.all()

    now = timezone.now()

    if (meeting.program_release_date is None
            or now < meeting.program_release_date) and \
            not request.user.is_superuser:
        return HttpResponseForbidden(
            'The participants list for %s will be (tentatively) released '
            'at %s' % (meeting.abbrv,
                       localtime(meeting.program_release_date).strftime(
                           '%c %Z'
                       ) if meeting.program_release_date else 'a future date'))

    attendee_list = Attendee.objects.filter(
        registration__meeting=meeting
    ).distinct().order_by('family_name')

    return render(request, 'asa18/meeting_participants.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(now),
                      'attendee_list': attendee_list,
                      'meeting_loc': meeting_loc,
                      'meeting_soc': meeting_soc,
                  })


def meeting_program(request, meeting):
    """
    Display the program of a meeting
    """

    now = timezone.now()

    meeting = get_object_or_404(Meeting, slug=meeting)

    if (meeting.program_release_date is None
            or now < meeting.program_release_date) and \
            not request.user.is_superuser:
        return HttpResponseForbidden(
            'The program for %s will be (tentatively) released '
            'at %s' % (meeting.abbrv,
                       localtime(meeting.program_release_date).strftime(
                           '%c %Z'
                       ) if meeting.program_release_date else 'a future date'))

    meetings = Meeting.objects.all()

    # Get all the talks, events and sessions linked to this meeting
    talks = Presentation.objects.filter(
        meeting=meeting, type='t',
    )
    sessions = Session.objects.filter(
        meeting=meeting
    )
    events = Event.objects.filter(
        meetings__in=[meeting, ]
    )

    if sessions.count() == 0 and events.count() == 0:
        return HttpResponseRedirect(meeting.get_absolute_url())

    # Now need to form the program structure for this meeting
    # This takes the form of a dict of lists of lists
    # The top-level dict maps a date to a list of lists
    # The master list contains all the events and sessions for that day;
    # the sub-lists show parallel sessions
    program_dict = {}
    curr_date = min(
        sessions[0].time_start if sessions.count() > 0 else
        now + datetime.timedelta(1e5),
        events[0].time_start if events.count() > 0 else
        now + datetime.timedelta(1e5),
    ).date()
    max_date = max(
        max([_.time_end for _ in sessions]).date() if sessions.count() > 0 else
        meeting.date_end,
        max([_.time_end for _ in events]).date() if events.count() > 0 else
        meeting.date_end,
    )
    while curr_date <= max_date:
        if (
            sessions.filter(
                time_start__year=curr_date.year,
                time_start__month=curr_date.month,
                time_start__day=curr_date.day,
            ).count() +
            events.filter(
                time_start__year=curr_date.year,
                time_start__month=curr_date.month,
                time_start__day=curr_date.day
            ).count()
        ) > 0:
            program_dict[curr_date] = []
            events_today = list(events.filter(
                time_start__year=curr_date.year,
                time_start__month=curr_date.month,
                time_start__day=curr_date.day
            ))
            sessions_today = list(sessions.filter(
                time_start__year=curr_date.year,
                time_start__month=curr_date.month,
                time_start__day=curr_date.day
            ))

            all_today = events_today + sessions_today
            # Order the sessions by time_start, time_end, and then the
            # *natural sort* of the session name
            all_today.sort(key=lambda x: (x.time_start,
                                          alphanum_key(x.title) if
                                          isinstance(x, Session) else
                                          alphanum_key(x.title()),
                                          x.time_end,
                                          ))
            # print 'All today list:'
            # print all_today

            while len(all_today) > 0:
                parallel_session = [all_today[0], ]
                dt_end = all_today[0].time_end
                all_today = all_today[1:]
                to_add = [None, ] # dummy
                while len(to_add) > 0:
                    to_add = [_ for _ in all_today if
                              _.time_start < dt_end]
                    parallel_session += to_add
                    all_today = [_ for _ in all_today if
                                 _ not in parallel_session]
                    dt_end = max([_.time_end for _ in parallel_session])
                parallel_session.sort(key=lambda x: x.time_start)
                program_dict[curr_date].append(parallel_session)

        # Advance the date
        curr_date += datetime.timedelta(1)

    # print program_dict
    program_dates = sorted(program_dict.keys())

    return render(request, 'asa18/meeting_program.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(now),
                      'talks': talks,
                      'program_dict': program_dict,
                      'program_dates': program_dates,
                  })


def meeting_posters(request, meeting):
    now = timezone.now()

    meeting = get_object_or_404(Meeting, slug=meeting)
    meetings = Meeting.objects.all()

    if (meeting.program_release_date is None
            or now < meeting.program_release_date) and \
            not request.user.is_superuser:
        return HttpResponseForbidden(
            'The program for %s will be (tentatively) released '
            'at %s' % (meeting.abbrv,
                       localtime(meeting.program_release_date).strftime(
                           '%c %Z'
                       ) if meeting.program_release_date else 'a future date'))

    # Get all the *accepted* posters attached to this meeting
    # If there aren't any, redirect to the meeting home page
    posters = meeting.get_accepted_posters().order_by('id_no', 'presenter')
    if posters.count() == 0:
        return HttpResponseRedirect(meeting.get_absolute_url())

    return render(request, 'asa18/meeting_posters.html',
                  {
                      'meeting': meeting,
                      'meetings': meetings,
                      'banner': get_banner(),
                      'now': now,
                      'rego_open': determine_rego_open(now),
                      'posters': posters,
                  })
