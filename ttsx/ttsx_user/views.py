#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from models import UserInfo
from hashlib import sha1
import datetime
# Create your views here.
def register(request):
    context={'title':'注册','top':'0'}
    return render(request,'ttsx_user/register.html',context)
def register_handle(request):
    #接收用户请求
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    ucpwd=post.get('user_cpwd')
    uemail=post.get('user_email')
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()
    #向数据库中保存数据
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd_sha1
    user.umail=uemail
    user.save()
    #重定向到登录页
    return redirect('/user/login/')
def register_valid(request):
    #接收用户名
    uname=request.GET.get('uname')
    #查询当前用户的个数
    data=UserInfo.objects.filter(uname=uname).count()
    #返回json{'valid':1或0}
    context={'valid':data}
    return JsonResponse(context)

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'登录','uname':uname,'top':'0'}
    return render(request,'ttsx_user/login.html',context)
def login_handle(request):
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('user_pwd')
    ujz=post.get('user_jz',0)

    s1=sha1()
    s1.update(upwd)
    upwd_sha1=s1.hexdigest()

    context = {'title': '登录','uname':uname,'upwd':upwd,'top':'0'}

    #如果没有查到数据则返回[]，如果查到数据则返回[UserInfo]
    result=UserInfo.objects.filter(uname=uname)
    if len(result)==0:
        #用户名不存在
        context['error_name']='用户名错误'
        return render(request,'ttsx_user/login.html',context)
    else:
        if result[0].upwd==upwd_sha1:
            #登录成功
            response = redirect('/user/')
            request.session['uid']=result[0].id
            #记住用户名
            if ujz=='1':
                response.set_cookie('uname',uname,expires=datetime.datetime.now() + datetime.timedelta(days = 14))
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:
            #密码错误
            context['error_pwd']='密码错误'
            return render(request, 'ttsx_user/login.html', context)

def center(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    context={'user':user}
    return render(request,'ttsx_user/center.html',context)
def order(request):
    context={}
    return render(request,'ttsx_user/order.html',context)
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':#post请求，修改当前用户对象的收货信息
        post=request.POST
        ushou=post.get('ushou')
        uaddress=post.get('uaddress')
        ucode=post.get('ucode')
        uphone=post.get('uphone')

        user.ushou=ushou
        user.uaddress=uaddress
        user.ucode=ucode
        user.uphone=uphone
        user.save()
    context={'user':user}
    return render(request,'ttsx_user/site.html',context)
