#!/usr/bin/python

import django
import sys
import os

if "/django/BHP" not in sys.path:
        sys.path.append("/django/BHP")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BHP.settings")

from BHP import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import logging
logger = logging.getLogger(__name__)

user_id = raw_input('Enter user id: ')
password = make_password(raw_input('Enter new password: '))

u = User.objects.get(id=int(user_id))

u.password=password
u.save()
