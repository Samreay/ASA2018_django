from django import template
from django.template.defaultfilters import stringfilter

from asa18.models import Event, Session

register = template.Library()


@register.filter(name='get_meeting_url')
def get_meeting_url(news_item, arg):
    return news_item.get_absolute_meeting_url(arg)


@register.filter(name='get_dict_item')
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='capitalize_family')
def capitalize_family(attendee, b):
    return attendee.full_name(capitalize_family=bool(b))


@register.filter(name='public_only_regooption')
def public_only_regooption(regooption_qs):
    return regooption_qs.filter(public=True)


@register.filter(name='max_time_end')
def max_time_end(list):
    return max([_.time_end for _ in list])


@register.filter(name='get_object_type')
def get_object_type(a):
    if isinstance(a, Event):
        return 'event'
    elif isinstance(a, Session):
        return 'session'
    else:
        return None


@register.filter(name='get_attendees_gender_pres')
def get_attendees_gender_pres(meeting, t):
    return meeting.generate_attendee_gender(presentation_type=t)


@register.filter(name='get_attendees_level_pres')
def get_attendees_level_pres(meeting, t):
    return meeting.generate_attendee_level(presentation_type=t)
