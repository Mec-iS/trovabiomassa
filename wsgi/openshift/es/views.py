from django.shortcuts import render_to_response
from django.template import RequestContext
from models import ProductCategory, Company, Fuel

import json

from django.views.decorators.csrf import ensure_csrf_cookie

from TrovaBiomassa import TrovaBiomassa, ToBuyBiomassFuels, productsList
from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.core.context_processors import csrf

@ensure_csrf_cookie
def home(request):
    params = {'products': []}
    # create array of product, see TB class
    params['products'] = productsList()  
    
    return render_to_response('es/home/home.html', params,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie   
def find(request, product=None, region= None, province=None):
    # create a TB class instance to handle the page
    instance = TrovaBiomassa()
    
    # initialize the instance with URL parameters
    instance.initialize({'product': str(product), 'region': str(region), 'province': str(province)})
    
    #turn the instance's variables into a dictionary
    params = instance.__dict__
    
    #the variable for the JS env are dumped to JSON
    params['regionsJSON'] = json.dumps(params['regions'])
    params['pdctsJSON']   = json.dumps(params['pdcts'])
    
    #cleaning the memory
    del instance
      
    return render_to_response('es/find/biomassa.html', params,
                              context_instance=RequestContext(request))


@ensure_csrf_cookie
def results(request, product=None, region= None, province=None):
    if request.method == 'GET':
        instance = TrovaBiomassa()

        instance.initialize({'product': str(product), 'region': str(region), 'province': str(province)})
        params = instance.__dict__
      
        params['path'] = request.path
        params['listed'] = instance.listed

        del instance
        params.update(csrf(request))
        return render_to_response('es/results/trovabiomassa.html', params,
                              context_instance=RequestContext(request))


@require_POST
def JsonProvider(request):
    if request.is_ajax():
        instance = TrovaBiomassa()
        instance.initialize({'product': request.POST['product'], 'region': request.POST['region'], 
                            'province': request.POST['province'] })
     
        j = instance.getMarkers()
                        
        del instance

        return StreamingHttpResponse(json.dumps(j), content_type="application/json")

@ensure_csrf_cookie
def bioshow(request, company, id, product):
    params = {}
    params['geolocate'] = ToBuyBiomassFuels(id, product)
    params['JSON'] = json.dumps(params['geolocate']['features'][0])
    params['product'] = product
       
    return render_to_response('es/results/bioshow.html', params,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie    
def coordinates(request):
    return render_to_response('es/coords.html',
                              context_instance=RequestContext(request))
        
        


