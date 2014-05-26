from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def privacy(request):
    return render_to_response('home/privacy.html',
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
def about(request):
    return render_to_response('home/about.html',
                              context_instance=RequestContext(request))

@ensure_csrf_cookie    
def energia(request):
    return render_to_response('home/energia.html',
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
def contacts(request):
    return render_to_response('home/contacts.html',
                              context_instance=RequestContext(request))
