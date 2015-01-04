# -*- coding: utf-8 -*-

import json
from uuid import uuid4
import time
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from articles.models import Article
from django.views.decorators.csrf import csrf_exempt

def generate_uuid():
    u = uuid4().hex
    return u

@csrf_exempt
def getArticles(request):
    result = {}
    articleList = []

    if request.method == 'GET':
        result['success'] = True
        try:
            tag = request.GET['tag']
            articles = Article.objects.filter(intention=tag)
            for article in articles:
                intent = article.intention
                uid = article.uid
                phone = article.cellphone
                title = article.title
                content = article.content
                a = {'intent':intent,'uid':uid,'phone':phone,'title':title,'content':content}
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
        intention = request.POST['intention']
        uid = generate_uuid()
        name = request.POST['username']
        cellphone = request.POST['cellphone']
        title = request.POST['title']
        content = request.POST['content']

        try:
            userArticle = Article(name=name,intention=intention,cellphone=cellphone,title=title,content=content,uid=uid,timestamp=time.time())
            # userArticle = Article(name="a",intention=1,cellphone='13716753743',title='title这是',content='content这是你',uid=uid,timestamp=time.time())
            userArticle.save()
        except Exception, e:
            result['success'] = False
            result['error'] = 'some error occured'

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
