from django.shortcuts import render_to_response
from django.template import RequestContext
from it.models import ProductCategory, Company, Fuel

import json

from django.views.decorators.csrf import ensure_csrf_cookie

from it.TrovaBiomassa import TrovaBiomassa, ToBuyBiomassFuels, productsList
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

@login_required
@ensure_csrf_cookie
def page(request):
    params = {}  
    
    return render_to_response('tmap/page.html', params,
                              context_instance=RequestContext(request))

