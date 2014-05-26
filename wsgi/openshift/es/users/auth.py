# users interactions

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from django.core.context_processors import csrf

from django.http import HttpRequest, StreamingHttpResponse
from django.core.mail import EmailMessage
from django.views.decorators.csrf import ensure_csrf_cookie

#from urllib import urlencode
from django import forms
#django.forms.models.model_to_dict.
#from captcha.fields import ReCaptchaField

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from es.models import ProductCategory, Company, Fuel

from django.core.exceptions import ValidationError

class SubrscriptionForm(forms.Form):
    sender = forms.EmailField(required=True, label='Email')
    name = forms.CharField(required=True, label='Nome')
    lastname = forms.CharField(required=True, label='Cognome')
    firm = forms.CharField(required=True, label='La Tua Azienda')
    phone = forms.CharField(required=False, label='Telefono(opzionale)')
    privacy = forms.BooleanField(required=True, label='Ho letto e accetto i termini per la privacy')
    #captcha = ReCaptchaField()

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        fields = ['reseller', 'product', 'package', 'producer', 'certification', 'selling_price',
                   'is_local', 'made_in_italy', 'made_in_eu', 'made_outside', 'specs']

class AddTransportForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('courier',)

@ensure_csrf_cookie
def subscription(request):
    if request.method == 'GET':
        params = {}
        form = SubrscriptionForm()
        params["form"] = form
        params.update(csrf(request))
        return render_to_response('es/users/register.html', params,
                              context_instance=RequestContext(request))

    if request.method == 'POST':
        form = SubrscriptionForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            firm = form.cleaned_data['firm']
            phone = form.cleaned_data['phone']

            to = "info@trovabiomassa.com"
            subject = "TrovaBiomassa: NUOVO UTENTE"
            content_txt = '''Qualcuno ha richiesto di registrarsi: \n
                       Nome:'''+name+'''\n  
                       Cognome: '''+lastname+'''\n
                       Azienda: '''+firm+'''\n
                       Email: '''+sender+'''\n
                       '''
            message = EmailMessage(subject, content_txt, to=[to])
            
            message.send()
            
            msg = {'message': 'grazie per esserti registrato, riceverai a breve tutte le informazioni necessarie per partecipare a TrovaBiomassa'}
            return render_to_response('es/users/register.html', msg,
                              context_instance=RequestContext(request))
        else:
            msg = {'message': 'Per favore completa correttamente i campi del form, e accetta i termini di utilizzo'}
            return render_to_response('es/users/register.html', msg,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
def newsletter(request):
    if request.method == 'POST':
        subscriber = request.POST['subscriber']

        to = "info@trovabiomassa.com"
        subject = "TrovaBiomassa: NUOVA RICHIESTA NEWSLETTER"
        content_txt = '''Qualcuno ha richiesto di iscriversi alla newsletter: \n
                       Email: '''+subscriber+'''\n
                       '''
        message = EmailMessage(subject, content_txt, to=[to])
            
        message.send()

        msg = {'message': 'grazie per esserti iscritto, riceverai il prossimo numero della nostra newsletter'}
        return render_to_response('es/users/register.html', msg,
                              context_instance=RequestContext(request))


@ensure_csrf_cookie
def login_user(request):
    state = ''
    username = '' 
    password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        params = {}
        form = SubrscriptionForm()
        params["form"] = form
        params.update(csrf(request))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                params = {}
                login(request, user)
                state = "Ti sei loggato!"
                return redirect('es.users.auth.main_profile')
            else:
                state = "Il suo account non &egrave; attivo, contattare un Amministratore"
        else:
            state = "<strong style='color:red;'>Nome o password non corretti</strong>"
    
    params = {'state':state, 'username': username}
    return render_to_response('es/users/login.html', params,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def main_profile(request):
    params = {'user' : request.user}
    query = Company.objects.all().filter(owner_of_account=request.user).exclude(region='Generico') # exclude from query geographical areas
    current_company = []
    i = 0
    for q in query:
        current_company.append(forms.models.model_to_dict(q))
        current_company[i]['products'] = []
        current_company[i]['courier'] = [c.name for c in q.courier.all()]
        query_products = Fuel.objects.all().filter(reseller=q.id).filter(selling=True)
        for p in query_products:
            current_company[i]['products'].append(p)
        i = i + 1     

    params['company'] = current_company
    
    return render_to_response('es/users/profile.html', params,
                              context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def remove_product(request, product_id):
    if request.method == 'GET':
        product_id = int(product_id)
        removing = Fuel.objects.get(id=product_id)
        current_user = request.user
        if current_user == removing.reseller.owner_of_account:
            params = {'p': removing}
            return render_to_response('es/users/remove_product.html', params,
                              context_instance=RequestContext(request))
        raise Http404

    if request.method == 'POST':
        product_id = request.POST.get('toremove')
        removing = Fuel.objects.all().get(id=product_id)
        current_user = request.user
        if current_user == removing.reseller.owner_of_account:
            removing.selling = False
            removing.save()
            return redirect('es.users.auth.main_profile')
        raise Http404

@ensure_csrf_cookie
@login_required
def modify_product(request, product_id, reseller_id):
    params = {}
    params['company_id'] = reseller_id
    product_id = int(product_id)
    current_user = request.user

    def get_form_data(pid):
        modifying = Fuel.objects.get(id=pid)
        form = FuelForm(instance=modifying)
        form.fields['producer'].queryset = Company.objects.all().filter(region='Generico') # load in queryset only geographical areas
        
        return form, modifying

    if request.method == 'GET':
        params["form"], obj = get_form_data(product_id)
        params.update(csrf(request))

        if current_user == obj.reseller.owner_of_account:
            params['p'] = obj
            return render_to_response('es/users/modify_product.html', params,
                              context_instance=RequestContext(request))
        raise Http404

    if request.method == 'POST':
        form = FuelForm(request.POST)
        form_data, obj = get_form_data(product_id)
        
        if form.is_valid():
            obj.selling = False
            obj.save()
            form.save()
            return redirect('es.users.auth.main_profile')
        else:
            mex = str(form.errors)+str(form.is_valid())
            params = {'message': 'Campi mancanti. Per favore completa correttamente il form:'+str(mex)}
            params['form'] = form_data
            params.update(csrf(request))
            params['p'] = obj
            return render_to_response('es/users/modify_product.html', params,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def add_product(request, reseller_id):
    params = {}
    params['company_id'] = reseller_id

    if request.method == 'GET':
        form = FuelForm()
        form.fields['producer'].queryset = Company.objects.all().filter(region='Generico') # load in queryset only geographical areas
        params["form"] = form
        params.update(csrf(request))
        return render_to_response('es/users/add_product.html', params,
                              context_instance=RequestContext(request))


    if request.method == 'POST':
        form = FuelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('es.users.auth.main_profile')
        else:
            params = {'message': '<strong>Campi mancanti. Per favore completa correttamente il form.</strong>'}
            form = FuelForm()

            params["form"] = form
            params.update(csrf(request))
            return render_to_response('es/users/add_product.html', params,
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def add_transport(request, reseller_id):
    if request.method == 'GET':
        params = {}
        params['company_id'] = reseller_id
        form = AddTransportForm()
        form.fields['courier'].queryset = Company.objects.all().filter(products_group__category=3)
        
        params["form"] = form
        params.update(csrf(request))
        return render_to_response('es/users/add_transport.html', params,
                              context_instance=RequestContext(request))


    if request.method == 'POST':
        s = get_object_or_404(Company, id=reseller_id)
        form = AddTransportForm(request.POST, instance = s)
        if form.is_valid():
            form.save()
            return redirect('es.users.auth.main_profile')
        else:
            params = {'message': '<strong>Campi mancanti. Per favore completa correttamente il form.</strong>'}
            form = AddTransportForm()
            params["form"] = form
            params.update(csrf(request))
            return render_to_response('es/users/add_transport.html', params,
                              context_instance=RequestContext(request))


@ensure_csrf_cookie
def logout_user(request):
  logout(request)
  return redirect('es.views.home')