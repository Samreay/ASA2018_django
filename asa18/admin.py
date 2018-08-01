# Django admin

from django.contrib import admin
from django.http import HttpResponse
from django import forms
from models import *

import csv
from django.utils.encoding import smart_str

from random import choice
from string import letters

# from mce_filebrowser.admin import admin.ModelAdmin

class RegoOptionInline(admin.TabularInline):
    model = RegoOption

class MeetingAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("abbrv", )
    }
    inlines = [
        RegoOptionInline,
    ]
    list_display = ['id', 'name', ]
    list_display_links = ('name', )
admin.site.register(Meeting, MeetingAdmin)


class RegoOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'meeting', 'opens', 'closes', 'cost_fmt')

    def cost_fmt(self, obj):
        return '$%.2f' % obj.cost
admin.site.register(RegoOption, RegoOptionAdmin)


class PolicyAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }
admin.site.register(Policy, PolicyAdmin)


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("title", )
    }
admin.site.register(News, NewsAdmin)

admin.site.register(Banner)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = []

    def clean(self):
        # If rego_closes is defined, make sure it occurs before the last
        # related event RegoOptions closes
        meetings = self.cleaned_data.get('meetings')
        limiting_rego_date = RegoOption.objects.filter(
            meeting__in=meetings).aggregate(
            models.Max('closes'))['closes__max']
        if limiting_rego_date is not None and self.cleaned_data.get('rego_closes') is not None:
            if self.cleaned_data.get('rego_closes') > limiting_rego_date:
                raise ValidationError('If a unique rego_closes date is '
                                      'specified for this event, it must be '
                                      '*before* the latest closing date of '
                                      'RegoOptions for the attached meeting(s) '
                                      '(%s)' % timezone.localtime(
                    limiting_rego_date).strftime(
                    '%Y-%m-%d %H:%M:%S'
                ))
        return


class EventOptionInline(admin.TabularInline):
    model = EventOption


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    prepopulated_fields = {
        "slug": ("name", )
    }
    inlines = [
        EventOptionInline,
    ]
admin.site.register(Event, EventAdmin)


class PrizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }
admin.site.register(Prize, PrizeAdmin)

admin.site.register(Sponsor)

class AttendeeAdmin(admin.ModelAdmin):
    def registered_for(obj):
        meetings = list(set(
            [_.meeting.abbrv for _ in Registration.objects.filter(attendee=obj)]
        ))
        return ', '.join(meetings)

    def all_paid(obj):
        cost = Decimal(0.)
        tot = Registration.objects.filter(attendee=obj).aggregate(
            tot_cost=Sum('meeting_rego__cost')
        )
        if tot['tot_cost'] is not None:
            cost += tot['tot_cost']
        tot = EventRegistration.objects.filter(attendee=obj).aggregate(
            tot_cost=Sum('event_option__cost')
        )
        if tot['tot_cost'] is not None:
            cost += tot['tot_cost']
        if cost == Decimal(0.):
            return True
        paid = Payment.objects.filter(attendee=obj).filter(
            is_paid=True
        ).aggregate(
            tot_paid=Sum('cost')
        )
        if paid['tot_paid'] is not None and paid['tot_paid'] >= cost:
            return True
        else:
            return False

    def payment_id(obj):
        try:
            payment = Payment.objects.filter(attendee=obj)[0]
            return payment.pk
        except:
            return 'No Payment ID'

    def export_csv(modeladmin, request, queryset):
        """
        From
        http://djangotricks.blogspot.com.au/2013/12/how-to-export-data-as-excel.html
        """
        def all_paid(obj):
            cost = Decimal(0.)
            tot = Registration.objects.filter(attendee=obj).aggregate(
                tot_cost=Sum('meeting_rego__cost')
            )
            if tot['tot_cost'] is not None:
                cost += tot['tot_cost']
            tot = EventRegistration.objects.filter(attendee=obj).aggregate(
                tot_cost=Sum('event_option__cost')
            )
            if tot['tot_cost'] is not None:
                cost += tot['tot_cost']
            if cost == Decimal(0.):
                return True
            paid = Payment.objects.filter(attendee=obj).filter(
                is_paid=True
            ).aggregate(
                tot_paid=Sum('cost')
            )
            if paid['tot_paid'] is not None and paid['tot_paid'] >= cost:
                return True
            else:
                return False
        def cost(obj):
            cost = Decimal(0.)
            tot = Registration.objects.filter(attendee=obj).aggregate(
                tot_cost=Sum('meeting_rego__cost')
            )
            if tot['tot_cost'] is not None:
                cost += tot['tot_cost']
            tot = EventRegistration.objects.filter(attendee=obj).aggregate(
                tot_cost=Sum('event_option__cost')
            )
            if tot['tot_cost'] is not None:
                cost += tot['tot_cost']

            return cost

        def payment_id(obj):
            try:
                payment = Payment.objects.filter(attendee=obj)[0]
                return payment.pk
            except:
                return ''

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode(
            'utf8'))  # BOM (optional...Excel needs it to open
                      # UTF-8 file properly)
        writer.writerow([
            smart_str(u"Attendee"),
            smart_str(u"Institution"),
            smart_str(u"Gender"),
            smart_str(u"Registered for"),
            smart_str(u"Email"),
            smart_str(u"Cost"),
            smart_str(u"All Paid"),
            smart_str(u"Payment ID"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.full_name(capitalize_family=True)),
                smart_str(obj.institution),
                smart_str(obj.gender),
                smart_str(list(set(
                    [_.meeting.abbrv for _ in Registration.objects.filter(attendee=obj)]
                ))),
                smart_str(obj.email),
                smart_str(cost(obj)),
                smart_str(all_paid(obj)),
                smart_str(payment_id(obj))                
            ])
        return response

    export_csv.short_description = u"Export CSV email list"
    actions = [export_csv, ]

    all_paid.boolean = True
    search_fields = ['family_name', 'given_names', 'city', 'email', ]
    list_display = ('__unicode__', 'family_name', registered_for, all_paid, payment_id)
admin.site.register(Attendee, AttendeeAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    def export_csv(modeladmin, request, queryset):
        """
        From
        http://djangotricks.blogspot.com.au/2013/12/how-to-export-data-as-excel.html
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode(
            'utf8'))  # BOM (optional...Excel needs it to open
                      # UTF-8 file properly)
        writer.writerow([
            smart_str(u"Meeting"),
            smart_str(u"Attendee"),
            smart_str(u"Email"),
            smart_str(u"Phone"),
            smart_str(u"Institution"),
            smart_str(u"Gender"),
            smart_str(u"Dietary restrictions (calculated from elsewhere, may not be complete!)"),
            smart_str(u"Rego. option")
        ])
        for obj in queryset:
            drs = DietaryRestriction.objects.filter(
                event_rego__attendee=obj.attendee
            )
            writer.writerow([
                smart_str(obj.meeting.abbrv),
                smart_str(obj.attendee.full_name(capitalize_family=True)),
                smart_str(obj.attendee.email),
                smart_str(obj.attendee.phone),
                smart_str(obj.attendee.institution),
                smart_str(obj.attendee.get_gender_display()),
                smart_str(
                    drs[0].pretty_print() if drs.count() > 0 else ""
                ),
                smart_str(obj.meeting_rego.name),
            ])
        return response

    export_csv.short_description = u"Export CSV"
    actions = [export_csv, ]

    def uc(obj):
        return obj.__unicode__()
    def pay_is_paid(obj):
        try:
            l = LineItem.objects.get(meeting_rego=obj)
        except LineItem.DoesNotExist:
            if obj.meeting_rego.cost <= Decimal(0.):
                return True
            return None
        if l.meeting_rego.meeting_rego.cost > Decimal(0.):
            return l.payment.is_paid
        else:
            return True
    pay_is_paid.boolean = True
    pay_is_paid.short_description = 'Is paid (computed)'
    uc.short_description = 'Registration'
    list_display = (uc, 'attendee', 'meeting', 'meeting_rego', 'is_paid',
                    pay_is_paid)
    search_fields = ['attendee__family_name', 'attendee__given_names',
                     'meeting__name', 'meeting__abbrv', ]
    list_filter = ['meeting', 'is_paid', ]
admin.site.register(Registration, RegistrationAdmin)

class PresentationAdminForm(forms.ModelForm):
    class Meta:
        model = Presentation
        # widgets = {
        #     'abstract': forms.Textarea,
        # }
        fields = '__all__'

class PresentationAdmin(admin.ModelAdmin):
    def export_csv(modeladmin, request, queryset):
        """
        From 
        http://djangotricks.blogspot.com.au/2013/12/how-to-export-data-as-excel.html
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode(
            'utf8'))  # BOM (optional...Excel needs it to open
                      # UTF-8 file properly)
        writer.writerow([
            smart_str(u"Attendee"),
            smart_str(u"Gender"),
            smart_str(u"Academic Level"),
            smart_str(u"Institution"),
            smart_str(u"Email"),
            smart_str(u"Title"),
            smart_str(u"Media"),
            smart_str(u"Abstract"),
            smart_str(u"Type"),
            smart_str(u"Status"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.presenter),
                smart_str(obj.presenter.gender),
                smart_str(obj.presenter.academic_level),
                smart_str(obj.presenter.institution),
                smart_str(obj.presenter.email),
                smart_str(obj.title),
                smart_str(obj.media),
                smart_str(obj.abstract),
                smart_str(obj.get_type_display()),
                smart_str(obj.get_status_display()),
            ])
        return response
    export_csv.short_description = u"Export CSV"

    def accept_all(modeladmin, request, queryset):
        for obj in queryset:
            obj.status = 'a'
            obj.save()
    accept_all.short_description = u"Accept all"

    def reject_all(modeladmin, request, queryset):
        for obj in queryset:
            obj.status = 'r'
            obj.save()
    reject_all.short_description = u"Reject all"

    actions = [export_csv, accept_all, reject_all, ]

    form = PresentationAdminForm

    list_display = ('meeting', 'generate_id', 'title', 'presenter', 'type',
                    'status', 'session', 'time_start', 'time_end', )
    list_display_links = ('title', )
    list_filter = ('type', 'status', 'meeting', )
    search_fields = ['presenter__family_name', 'presenter__given_names',
                     'title', ]

admin.site.register(Presentation, PresentationAdmin)

class DietaryRestrictionAdmin(admin.ModelAdmin):
    raw_id_fields = ['event_rego', ]
    search_fields = ['event_rego__event__name',
                     'event_rego__attendee__family_name',
                     'event_rego__attendee__given_names']
admin.site.register(DietaryRestriction, DietaryRestrictionAdmin)

class DietaryRestrictionInline(admin.TabularInline):
    model = DietaryRestriction
class EventRegistrationAdmin(admin.ModelAdmin):
    def export_csv(modeladmin, request, queryset):
        """
        From
        http://djangotricks.blogspot.com.au/2013/12/how-to-export-data-as-excel.html
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode(
            'utf8'))  # BOM (optional...Excel needs it to open
                      # UTF-8 file properly)
        writer.writerow([
            smart_str(u"Event"),
            smart_str(u"Attendee"),
            smart_str(u"Email"),
            smart_str(u"Institution"),
            smart_str(u"Extra guests"),
            smart_str(u"Total guests"),
            smart_str(u"Dietary restrictions (separate persons "
                      u"separated by ; )"),
            smart_str(u"Extra comments"),
        ])
        for obj in queryset:
            drs = obj.dietaryrestriction_set.all()
            writer.writerow([
                smart_str(obj.event.name),
                smart_str(obj.attendee.full_name(capitalize_family=True)),
                smart_str(obj.attendee.email),
                smart_str(obj.attendee.institution),
                smart_str(obj.event_option.extra_guests),
                smart_str(obj.event_option.extra_guests + 1),
                smart_str(
                    ' ; '.join([_.pretty_print() for _ in drs])
                ),
                smart_str(obj.extra_comments),
            ])
        return response

    export_csv.short_description = u"Export CSV"
    actions = [export_csv, ]

    def uc(obj):
        return obj.__unicode__()

    uc.short_description = 'Registration'

    def pay_is_paid(obj):
        try:
            l = LineItem.objects.get(event_rego=obj)
        except LineItem.DoesNotExist:
            if obj.event_option.cost <= Decimal(0.):
                return True
            return None
        if l.event_rego.event_option.cost > Decimal(0.):
            return l.payment.is_paid
        else:
            return True
    pay_is_paid.boolean = True
    pay_is_paid.short_description = 'Is paid (computed)'
    search_fields = ['attendee__family_name', 'attendee__given_names',
                     'event__name', ]
    inlines = (DietaryRestrictionInline, )
    list_display = (uc, 'attendee', 'event', 'event_option', 'is_paid',
                    pay_is_paid
                    # 'lineitem'
                    )
    list_filter = ['event', 'event_option', ]
admin.site.register(EventRegistration, EventRegistrationAdmin)

class LineItemAdmin(admin.ModelAdmin):
    search_fields = ['attendee__given_names', 'attendee__family_name',
                     'meeting_rego__meeting__name',
                     'event_rego__event__name', ]
admin.site.register(LineItem, LineItemAdmin)

class PaymentAdmin(admin.ModelAdmin):
    def uc(obj):
        return obj.__unicode__()
    uc.short_description = 'Payment ID'
    list_display = (uc, 'attendee', 'cost', 'is_paid')
    search_fields = ['order_id', 'attendee__given_names',
                     'attendee__family_name', ]
admin.site.register(Payment, PaymentAdmin)


class SessionAdmin(admin.ModelAdmin):
    def uc(obj):
        return obj.__unicode__()
    uc.short_description = 'Session'

    def meeting_abbrv(obj):
        return obj.meeting.abbrv
    meeting_abbrv.short_description = 'Meeting'

    search_fields = ['title', 'meeting__name', 'location', 'blurb', ]
    list_display = (meeting_abbrv, 'title', 'blurb', 'time_start', 'time_end',
                    'chair', 'location', )
    list_display_links = ('title', )
    list_filter = ['meeting', ]
    date_hierarchy = 'time_start'
admin.site.register(Session, SessionAdmin)
