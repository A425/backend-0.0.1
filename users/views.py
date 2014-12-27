import json

from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def createUser(request):
    result = {}

    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']

        try:
            newUser = User.objects.create_user(username=name,password=password)
            result['success'] = True
            result['user'] = name
            newUser.save()
            print newUser
        except Exception, e:
            result['success'] = False
            result['exception'] = e
            print e

    return JsonResponse(result)

@csrf_exempt
def signIn(request):
    result = {}

    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']

        try:
            if name and password:
                user = authenticate(username=name, password=password)
                if user.is_active:
                    login(request, user)
                    result['success'] = True
                else:
                    result['success'] = False
            else:
                result['success'] = False
        except Exception, e:
            result['success'] = False
            result['exception'] = e

    return JsonResponse(result)

@csrf_exempt
def testData(request):
    result = {}

    if request.method == 'GET':
        result['success'] = True
        result['username'] = 'Liuyuchen'

    return JsonResponse(result)

