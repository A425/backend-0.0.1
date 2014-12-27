import json

from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

#code 100 == user exist
#code 101 == error when create
#code 102 == name or pw incorrect
#code 103 == name or pw blank
#code 104 == error when signin
#code 105 == password and confirm password does not match

@csrf_exempt
def createUser(request):
    result = {}

    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm
            result['success'] = False
            result['code'] = 105
            return JsonResponse(result)

        try:
            User.objects.get(username=name)
            result['success'] = False
            result['code'] = 100
        except User.DoesNotExist:
            try:
                newUser = User.objects.create_user(username=name,password=password)
                result['success'] = True
                result['user'] = name
                newUser.save()
                print newUser
            except Exception, e:
                result['success'] = False
                result['code'] = 101
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
                if user is not None:
                    login(request, user)
                    result['success'] = True
                    result['user'] = name
                else:
                    result['success'] = False
                    result['code'] = 102
            else:
                result['success'] = False
                result['code'] = 103
        except Exception, e:
            result['success'] = False
            result['code'] = 104

    return JsonResponse(result)

@csrf_exempt
def testData(request):
    result = {}

    if request.method == 'GET':
        result['success'] = True
        result['username'] = 'Liuyuchen'

    return JsonResponse(result)

