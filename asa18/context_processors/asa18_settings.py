from django.conf import settings

def asa18_settings(request):
    settings_dict = {
        'REGISTRATION_EMAIL': settings.REGISTRATION_EMAIL,
        'STRIPE_KEY_PUBLISHABLE': settings.STRIPE_KEY_PUBLISHABLE,
        'GLOBAL_PAGE_TITLE': settings.GLOBAL_PAGE_TITLE,
    }
    return settings_dict
