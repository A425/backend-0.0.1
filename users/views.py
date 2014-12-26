import json

from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.contrib.auth.models import User

def createUser(request):
    result = {}

    print 'Before'
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')

        print name
        print password
        try:
            newUser = User.objects.create_user(username=name,password=password)
            result['success'] = True
            result['user'] = newUser
            print newUser
        except Exception, e:
            result['success'] = False
            result['exception'] = e
            print e

    print 'End'
    return HttpResponse(str(result), content_type="application/json")

def signIn(request):
    result = {}

    name = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        user = authenticate(username=name, password=password)
        if user.is_active:
            login(request, user)
            result['success'] = True
        else:
            result['success'] = False
    else:
        result['success'] = False

    return HttpResponse(str(result), content_type="application/json")

