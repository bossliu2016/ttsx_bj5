#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
# Create your views here.
def index(request):
    type_list=TypeInfo.objects.all()
    list1=[]
    for type1 in type_list:
        new_list=type1.goodsinfo_set.order_by('-id')[0:4]
        click_list=type1.goodsinfo_set.order_by('-gclick')[0:4]
        list1.append({'new_list':new_list,'click_list':click_list,'t1':type1})
    context={'list1':list1,'title':'首页','cart_show':'1'}
    return render(request,'ttsx_goods/index.html',context)

def goods_list(request,tid,pindex,orderby):
    t1=TypeInfo.objects.get(pk=int(tid))
    orderby_str='-id'#默认排序，根据id降序
    desc='1'
    if int(orderby)==2:#根据价格排序
        desc=request.GET.get('desc')
        if desc=='1':
            orderby_str = '-gprice'
        else:
            orderby_str = 'gprice'
    elif int(orderby)==3:#根据人气降序
        orderby_str='-gclick'
    new_list=t1.goodsinfo_set.order_by('-id')[0:2]
    glist=t1.goodsinfo_set.order_by(orderby_str)
    paginator=Paginator(glist,10)
    pindex1=int(pindex)
    if pindex1<=1:
        pindex1=1
    if pindex1>=paginator.num_pages:
        pindex1=paginator.num_pages
    page=paginator.page(pindex1)
    context={'cart_show':'1','title':'商品列表','t1':t1,'new_list':new_list,'page':page,'orderby':orderby,'desc':desc}
    return render(request,'ttsx_goods/list.html',context)

def detail(request,id):
    try:
        goods=GoodsInfo.objects.get(pk=int(id))
        goods.gclick+=1
        goods.save()
        #找到当前商品的分类对象，再找到所有此分类的商品中最新的两个
        new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context={'cart_show':'1','title':'商品详细信息','new_list':new_list,'goods':goods}
        response=render(request, 'ttsx_goods/detail.html', context)
        # 最近浏览[]<-->1,2,3,4,5
        ids=request.COOKIES.get('goods_ids','').split(',')
        if id in ids:
            ids.remove(id)
        ids.insert(0,id)
        if len(ids)>5:
            ids.pop()
        response.set_cookie('goods_ids',','.join(ids),max_age=60*60*24*7)
        return response
    except:
        return render(request,'404.html')
