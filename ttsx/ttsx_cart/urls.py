from django.conf.urls import url
import views
urlpatterns=[
    url('^$',views.index),
    url('^add/$',views.add),
    url('^count/$',views.count),
    url('^edit/$',views.edit),
    url('^del/$',views.delete),
    url('^order/$',views.order),
]
