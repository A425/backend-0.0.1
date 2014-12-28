import json
from uuid import uuid4

from django.contrib.auth import authenticate, login, logout
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from django.contrib.auth.models import User
# from users.models import Token
from django.views.decorators.csrf import csrf_exempt

#code 100 == user exist
#code 101 == error when create
#code 102 == name or pw incorrect
#code 103 == name or pw blank
#code 104 == error when signin
#code 105 == password and confirm password does not match
#code 106 == token validate is fail need signin

def generate_uuid():
    u = uuid4().hex
    return u

# @csrf_exempt
# def userValidate(request):
#      result = {}
#      if request.method == 'POST':
#         token = request.POST['token']
#         name = request.POST['username']

#         try:
#             Token.objects.get(name=name,token=token)
#             result['success'] = True
#             result['user'] = name
#         except Token.DoesNotExist:
#             result['success'] = False
#             result['code'] = 106

#         return JsonResponse(result)


@csrf_exempt
def createUser(request):
    result = {}

    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if name =='' or password =='':
            result['success'] = False
            result['code'] = 103
            return JsonResponse(result)

        if password != confirm:
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
                login(request, newUser)
                result['success'] = True
                result['user'] = name
                newUser.save()
                # token = generate_uuid()
                # userToken = Token(name=name,token=token)
                # userToken.save()
                # result['token'] = token
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
                    # userToken = Token.objects.get(name=name)
                    # userToken.token = generate_uuid()
                    # result['token'] = userToken.token
                    # userToken.save()
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

