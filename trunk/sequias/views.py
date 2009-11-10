from django.shortcuts import render_to_response
from sequia.sequias.models import *
from django.conf import settings

def index(request):
    return render_to_response('base.html')
