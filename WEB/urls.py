"""
Definition of urls for WEB.
"""

from datetime import datetime
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
admin.autodiscover()

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('pool/', views.pool, name='pool'),
    path('links/', views.links, name='links'),
    path('blog/', views.blog, name='blog'),
    path('newpost/', views.newpost, name='newpost'),
    path('video/', views.videopost, name='videopost'),
    path(r'^<int:parametr>/$', views.blogpost, name='blogpost'),
    path('regisration/', views.registration, name='registration'),
    path('regisration_provider/', views.registration_provider, name='registration_provider'),
    path('cart/', views.cart, name='cart'),
    path(r'cart/^<id>\/$', views.addtocart, name='addtocart'),
    path('buy/<bid>/', views.buy, name='buy'),
    path('paying/<bid>/', views.paying, name='paying'),
    path('payed/<bid>/', views.payed, name='payed'),
    path('finances/', views.finances, name='finances'),
    path('onemore/<nid>', views.onemore, name='onemore'),
    path('oneless/<pid>', views.oneless, name='oneless'),    
    path('onemoreproduct/<pid>', views.onemoreproduct, name='onemoreproduct'),
    path('onelessproduct/<pid>', views.onelessproduct, name='onelessproduct'),
    path('onemoreproductmanage/<pid>', views.onemoreproductmanage, name='onemoreproductmanage'),
    path('onelessproductmanage/<pid>', views.onelessproductmanage, name='onelessproductmanage'),
    path('delcart/<did>/', views.delcart, name='delcart'),
    path('order/<did>/', views.order, name='order'),
    path('orders/', views.completeorders, name='completeorders'),
    path('allorders/', views.allorders, name='allorders'),
    path('onemoremanage/<nid>', views.onemoremanage, name='onemoremanage'),
    path('onelessmanage/<pid>', views.onelessmanage, name='onelessmanage'),
    path('buymanage/<bid>/', views.buymanage, name='buymanage'),
    path('unbuymanage/<bid>/', views.unbuymanage, name='unbuymanage'),
    path('delcartmanage/<did>/', views.delcartmanage, name='delcartmanage'),
    path('delproductmanage/<did>/', views.delproductmanage, name='delproductmanage'),
    path('newproduct/', views.newproduct, name='newproduct'),
    path('nope/', views.nope, name='nope'),

    path('admin/', admin.site.urls),
    path('login/',
            LoginView.as_view
            (
                template_name='app/login.html',
                authentication_form=forms.BootstrapAuthenticationForm,
                extra_context=
                {
                    'title': 'Войти',
                    'year' : datetime.now().year,
                }
            ),
            name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
