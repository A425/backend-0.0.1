from django.http import HttpResponse
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import cookielib, urllib, re, os, webbrowser
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import StringIO
import json
from django.views.decorators.csrf import csrf_exempt

loginUrl = "http://gdjwgl.bjut.edu.cn/"
loginServer = "default2.aspx"

checkcodeURL = loginUrl + 'CheckCode.aspx'

# # save the checkcode to local
# checkcodeCachePath = '/Users/liuyuchen/Documents/checkcodeCache.gif'

# # main page
# mainPageUrl = 'http://gdjwgl.bjut.edu.cn/xs_main.aspx?xh=11090308'
mainPageUrl = loginUrl + 'xs_main.aspx?xh='

# # score
# scorePageUrl = 'http://gdjwgl.bjut.edu.cn/xscjcx.aspx?xh=11090308&xm=%C1%F5%D3%EA%B3%BF&gnmkdm=N121605'
scorePageUrl = loginUrl + 'xscjcx.aspx?xh='

scorePageSuffix = '&xm=%C1%F5%D3%EA%B3%BF&gnmkdm=N121605'

#Create a CookieJar object to hold the cookies
cj = cookielib.CookieJar()
#Create an opener to open pages using the http protocol and to process cookies.
opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

def hello(request):
    return HttpResponse("Hello world")

def getCheckCode(request):

    checkcodePic = opener.open(checkcodeURL).read()
    return HttpResponse(checkcodePic)

@csrf_exempt
def register(request):
    content = {}
    if request.method == 'POST':
        uname = request.POST['username']
        pw = request.POST['password']

        content['username'] = uname
        content['password'] = pw

        print content

    return HttpResponse(str(content), content_type="application/json")


@csrf_exempt
def login(request):

    # #Create a CookieJar object to hold the cookies
    # cj = cookielib.CookieJar()
    # #Create an opener to open pages using the http protocol and to process cookies.
    # opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())

    # # GET the checkcode
    # checkcodePic = opener.open(checkcodeURL).read()
    # f = file(checkcodeCachePath,'wb')
    # f.write(checkcodePic)
    # f.close()

    # icode = raw_input('Plesea enter the checkcode \n')
    # print 'the checkcode is' , icode

    stuId = ''
    pw = ''
    checkCode = ''

    if request.method == 'POST':
        stuId = request.POST['stuId']
        pw = request.POST['pw']
        checkCode = request.POST['checkCode']

    #create a request object to be used to get the page.
    req = Request(loginUrl + loginServer)
    f = opener.open(req)

    viewstate = re.compile(r'name="__VIEWSTATE" value="(.*?)" /',re.DOTALL)

    try:
        viewstate = viewstate.search(f.read()).group(1)
    except:
        print 'cannot find the value of viewstate'

    # login data
    loginData = {
        '__VIEWSTATE': str(viewstate),
        'txtUserName': str(stuId),
        'TextBox2': str(pw),
        'txtSecretCode': str(checkCode),
        'RadioButtonList1':'%D1%A7%C9%FA',
        'Button1':'',
        'lbLanguage':'',
        'hidPdrs':'',
        'hidsc':''
    }
    # print loginData
    print loginData

    # request object
    loginRequest = Request(loginUrl+loginServer, urllib.urlencode(loginData))
    cj.add_cookie_header(loginRequest)
    # print loginRequest.get_header('Cookie')

    # LOGIN: HTTP POST
    loginResponse = opener.open(loginRequest)

    # get viewstate
    searchHeader = {
        'Referer':mainPageUrl + stuId
    }

    scoreUrl = scorePageUrl + stuId + scorePageSuffix

    mainPageRequest = Request(scoreUrl, headers = searchHeader)
    cj.add_cookie_header(mainPageRequest)
    mainPageHTML = opener.open(mainPageRequest).read()

    contentViewstate = re.compile(r'name="__VIEWSTATE" value="(.*?)" /',re.DOTALL)
    try:
        contentViewstate = contentViewstate.search(mainPageHTML).group(1)
    except:
        print 'cannot find the value of viewstate'

    # post get content
    contentHeader = {
        'Referer':scoreUrl
    }
    contentData = {
        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE': str(contentViewstate),
        'hidLanguage':'',
        'ddlXN':'',
        'ddlXQ':'',
        'ddl_kcxz':'',
        'btn_zcj':'%C0%FA%C4%EA%B3%C9%BC%A8'
    }

    contentPageRequest = Request(scoreUrl, urllib.urlencode(contentData), contentHeader)
    cj.add_cookie_header(contentPageRequest)
    contentPageHtml = opener.open(contentPageRequest).read()

    soup = BeautifulSoup(contentPageHtml)
    result = soup.find_all('table', class_='datelist')
    result = str(result)

    # get the detail of the user
    detail = ur'<td>\d{4}-\d{4}</td><td>.+</td>'
    detail = re.findall(detail, result)

    # credit of the user
    credit = []
    # G point of the user
    gpoint = []
    # score of the user
    score = []

    for x in xrange(0,len(detail)):
        soup = BeautifulSoup(detail[x])
        res = soup.find_all('td')
        credit.append(str(res[6]).replace("<td>","").replace("</td>",""))
        gpoint.append(str(res[7]).replace("<td>","").replace("</td>",""))
        score.append(str(res[8]).replace("<td>","").replace("</td>",""))

    content = {}
    content['credit'] = credit
    content['gpoint'] = gpoint
    content['score'] = score

    return HttpResponse(str(content), content_type="application/json")
