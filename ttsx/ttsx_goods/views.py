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

def goods_list(request,tid,pindex):
    t1=TypeInfo.objects.get(pk=int(tid))
    new_list=t1.goodsinfo_set.order_by('-id')[0:2]
    glist=t1.goodsinfo_set.order_by('-id')
    paginator=Paginator(glist,1)
    page=paginator.page(int(pindex))
    context={'cart_show':'1','title':'商品列表','t1':t1,'new_list':new_list,'page':page}
    return render(request,'ttsx_goods/list.html',context)

def detail(request,id):
    try:
        goods=GoodsInfo.objects.get(pk=int(id))
        goods.gclick+=1
        goods.save()
        #找到当前商品的分类对象，再找到所有此分类的商品中最新的两个
        new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context={'cart_show':'1','title':'商品详细信息','new_list':new_list,'goods':goods}
        return render(request,'ttsx_goods/detail.html',context)
    except:
        return render(request,'404.html')
