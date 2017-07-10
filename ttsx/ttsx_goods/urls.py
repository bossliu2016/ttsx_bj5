from django.conf.urls import url
import views
from search_view import *
urlpatterns=[
    url('^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.goods_list),
    url(r'^(\d+)/$',views.detail),
    url('^search/$',MySearchView.as_view())
]
