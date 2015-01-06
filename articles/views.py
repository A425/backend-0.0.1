# -*- coding: utf-8 -*-

import json
from uuid import uuid4
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import smart_unicode
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from articles.models import Article
from users.models import Token

#code 106 == token validate is fail need signin

def generate_uuid():
    u = uuid4().hex
    return u

@csrf_exempt
def getMatrixCode(request):
    if request.method == 'GET':
        image_data = open(settings.IMAGE_BASEDIR+"/download.png", "rb").read()
        return HttpResponse(image_data, content_type="image/png")

@csrf_exempt
def getArticles(request):
    result = {}
    articleList = []

    if request.method == 'GET':
        result['success'] = True
        try:
            tag = request.GET.get('tag','')
            timestamp = request.GET.get('ts','')
            articles = Article.objects.filter(intention=tag, timestamp__gt=timestamp)
            for article in articles:
                intent = article.intention
                uid = article.uid
                phone = article.cellphone
                title = article.title
                content = article.content
                timestamp = article.timestamp
                a = {'intent':intent,'uid':uid,'phone':phone,'title':title,'content':content,'timestamp':str(timestamp)}
                articleList.append(a)
            result['list'] = articleList
                # get all post
        except Article.DoesNotExist:
            result['error'] = 'article not found'
            result['success'] = False

    return JsonResponse(result)


@csrf_exempt
def postArticle(request):
    result = {}

    if request.method == 'POST':
        result['success'] = True
        intention = request.POST.get('intention','')
        uid = generate_uuid()
        name = request.POST.get('username','')
        cellphone = request.POST.get('cellphone','')
        title = smart_unicode(request.POST.get('title',''))
        content = request.POST.get('content','')
        token = request.POST.get('token','')

        try:
            Token.objects.get(name=name,token=token)
            now = time.time()*1000
            userArticle = Article(name=name,intention=intention,cellphone=cellphone,title=title,content=content,uid=uid,timestamp=str('%.0f'%now))
            # userArticle = Article(name="a",intention=1,cellphone='13716753743',title='title这是',content='content这是你',uid=uid,timestamp=time.time())
            userArticle.save()
        except Token.DoesNotExist:
            result['success'] = False
            result['code'] = 106

    return JsonResponse(result)


@csrf_exempt
def testArticle(request):
    result = {}

    if request.method == 'GET':
        result['success'] = True
        name = 'Liuyuchen'

        intention = 1
        cellphone = '13716753743'
        title = 'Oh God!'
        content = 'where is my freaking purse!'

        userArticle = Article(name=name,intention=intention,cellphone=cellphone,title=title,content=content,timestamp=time.time())
        userArticle.save()
        # userToken = Token.objects.get(name=name)
        # userToken.token = generate_uuid()
        # result['token'] = userToken.token
        # userToken.save()

    return JsonResponse(result)
