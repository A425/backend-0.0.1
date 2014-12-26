import json

from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def createUser(request):
    result = {}

    if request.method == 'POST':
        req = json.loads(request.body)
        name = req.get('username', '')
        password = req.get('password', '')

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

    return HttpResponse(str(result), content_type="application/json")

@csrf_exempt
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

