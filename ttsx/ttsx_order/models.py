from django.db import models
from ttsx_user.models import UserInfo
from ttsx_goods.models import GoodsInfo
# Create your models here.

class OrderMain(models.Model):
    #1 2 3 4
    orderid=models.CharField(max_length=20,primary_key=True)#20170713000000用户id
    order_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(UserInfo)
    total=models.DecimalField(max_digits=8,decimal_places=2)

class OrderDetail(models.Model):
    order=models.ForeignKey(OrderMain)
    goods=models.ForeignKey(GoodsInfo)
    count=models.IntegerField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
