"""
WSGI config for BHP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

if "/usr/local/lib/python2.7/dist-packages/django_mobile" not in sys.path:
        sys.path.append("/usr/local/lib/python2.7/dist-packages/django_mobile")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
