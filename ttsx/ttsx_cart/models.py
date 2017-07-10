from django.db import models
from ttsx_user.models import UserInfo
# Create your models here.
class CartInfo(models.Model):
    goods=models.ForeignKey('ttsx_goods.GoodsInfo')
    user=models.ForeignKey(UserInfo)
    count=models.IntegerField()
