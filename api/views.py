# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
import json
import logging

logger = logging.getLogger(__name__)

def login(request):
    try:
        data = json.loads(request.body)
    except:
        resp = {"error": -1, "msg": "An error occurred decoding the payload"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    username = data["username"]
    password = data["password"]

    if username is None or password is None:
        resp = {"error": -1, "msg": "Username and password are both required fields"}
        return HttpResponse(json.dumps(resp), content_type="application/json")

    user = authenticate(username=username, password=password)
    if user is not None:
        resp = {"error": 0, "player_id": user.id}
    else:
        resp = {"error": -1, "msg": "Invalid username or password"}

    return HttpResponse(json.dumps(resp), content_type="application/json")
