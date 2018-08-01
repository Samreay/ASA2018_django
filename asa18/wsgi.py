"""
WSGI config for asa18 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asa18.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# import asa18.monitor
# asa18.monitor.start(interval=1.0)

