import logging
from forum.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from forms import ClassicRegisterForm
from forum.views.auth import login_and_forward
from forum.actions import UserJoinsAction
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.cache import cache
from forum.authentication import AUTH_PROVIDERS

BANNED_EMAILS_KEY = 'banned_emails_key'
BANNED_IPS_KEY = 'banned_ips_key'
BAN_CACHE_TIMEOUT = 86400


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def ban(email, ip):
    banned_emails = cache.get(BANNED_EMAILS_KEY, set())
    banned_emails.add(email)
    cache.set(BANNED_EMAILS_KEY, banned_emails, BAN_CACHE_TIMEOUT)
    banned_ips = cache.get(BANNED_IPS_KEY, set())    
    banned_ips.add(ip)    
    cache.set(BANNED_IPS_KEY, banned_ips, BAN_CACHE_TIMEOUT)
    
def _get_bigicon_providers(request):
    all_providers = [provider.context for provider in AUTH_PROVIDERS.values() if provider.context]

    sort = lambda c1, c2: c1.weight - c2.weight
    can_show = lambda c: not request.user.is_authenticated() or c.show_to_logged_in_user

    return sorted([context for context in all_providers if context.mode == 'BIGICON' and can_show(context)], sort)

def register(request):
    banned_ips = cache.get(BANNED_IPS_KEY, set())
    ip = get_client_ip(request)
    if ip in banned_ips:
        logging.warning("Spammer returned ip:%s" % ip)
        return HttpResponseRedirect('http://www.pudelek.pl/artykul/x/')
    
    if request.method == 'POST':        
        banned_emails = cache.get(BANNED_EMAILS_KEY, set())
        if request.POST['email'] in banned_emails:
            logging.warning("Spammer returned:%s, ip:%s" % (request.POST['email'], ip))
            return HttpResponseRedirect('http://www.pudelek.pl/artykul/x/')
        
        form = ClassicRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            
            #Honeypot checks
            if request.POST.get('age', None):
                logging.warning("Age honeypot filled, will not register for email:%s, ip:%s" % (email, ip))
                ban(email, ip)
                return HttpResponseRedirect(reverse('index'))
        
            if request.POST.get('birthday', None):
                logging.warning("Birthday honeypot filled, will not register for email:%s, ip:%s" % (email, ip))
                ban(email, ip)
                return HttpResponseRedirect(reverse('index'))
            
            if request.POST.get('website', None):
                logging.warning("Website honeypot filled, will not register for email:%s, ip:%s" % (email, ip))
                ban(email, ip)
                return HttpResponseRedirect(reverse('index'))
            
            user_ = User(username=username, email=email)
            user_.set_password(password)

            if User.objects.all().count() == 0:
                user_.is_superuser = True
                user_.is_staff = True

            user_.save()
            UserJoinsAction(user=user_, ip=request.META['REMOTE_ADDR']).save()
            logging.info("New user joined with email:%s from ip:%s" % (email, ip) )

            return login_and_forward(request, user_, None, _("A welcome email has been sent to your email address. "))
    else:
        form = ClassicRegisterForm(initial={'next':'/'})

    return render_to_response('auth/register.html', {
        'form1': form,
        'bigicon_providers' : _get_bigicon_providers(request)
        }, context_instance=RequestContext(request))
