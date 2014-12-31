import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from articles.models import Article
from django.views.decorators.csrf import csrf_exempt

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

        userArticle = Article(name=name,intention=intention,cellphone=cellphone,title=title,content=content)
        userArticle.save()
        result['result'] = userArticle

        # userToken = Token.objects.get(name=name)
        # userToken.token = generate_uuid()
        # result['token'] = userToken.token
        # userToken.save()

    return JsonResponse(result)
