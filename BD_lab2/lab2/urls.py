from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^edit/(?P<id>[\w]+)/$', views.edit, name='edit_page'),
    url(r'^add/$', views.add, name='add_page'),
    url(r'^remove/(?P<id>[\w]+)/$', views.remove),
    url(r'^$', views.main, name='main_page'),
    url(r'^top$', views.topproducts, name='top_products'),
]
