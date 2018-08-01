# Assorted helper functions

from .models import *

import random
import re


def get_banner():
    """
    Return a banner image location
    """
    no_banner = Banner.objects.count()
    if no_banner > 0:
        i_banner = random.randint(0, no_banner - 1)
        banner = Banner.objects.all()[i_banner]
        return banner
    return None


def determine_rego_open(now):
    """
    Determine the date when the current/next tranche of regos opens and closes
    """
    options_open = RegoOption.objects.filter(opens__lte=now,
                                             closes__gte=now).count()
    if options_open > 0:
        return True
    return False


def get_meeting_attendees(meeting):
    # Get all the registrations for this meeting
    meetings_regos = Registration.objects.filter(meeting=meeting)
    attendees = list(set([mr.attendee for mr in meetings_regos]))
    return attendees


def generate_registration_summary(meeting):
    """Generate a JSON string detailing registration info for the 
    requested meeting"""
    return
    # Assume meeting is already a singular Meeting object


# The following two functions to provide a 'natural sort' (that is, a more
# human alphabetical sort
# Note this should only be used on small (tens to hundreds) QuerySets,
# otherwise it becomes inefficient
# See:
# https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
# https://nedbatchelder.com/blog/200712.html#e20071211T054956

def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)