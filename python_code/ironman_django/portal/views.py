from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def index(request):
    return render(request,'portal/index.html')



def auth(request):
    usr = request.POST['usr']
    psd = request.POST['psd']
    user = authenticate(username=usr,password=psd)

    if user is not None and user.is_active:
        login(request,user)
        return HttpResponseRedirect('/portal')
    else:
        return HttpResponseRedirect('/')

@login_required
def portal(request):
    context = {}
    context['loginUser'] = request.user.username
    return render(request,'portal/portal.html',context)



def test(request):
    return render(request,'portal/test.html')
