"""election URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from election2000 import views
from election import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^Polska/$', views.country),
    url(r'^Polska/(?P<voivodeship>(?:\w|-)+)/$', views.voivodeship),
    url(r'^Polska/(?P<voivodeship>(?:\w|-)+)/(?P<district>\w+)/$', views.district),
    url(r'^Polska/(?P<voivodeship>(?:\w|-)+)/(?P<district>\d+)/(?P<gmina>[^\/]+)/$',
        views.gmina),
    url(r'^Polska/(?P<voivodeship>(?:\w|-)+)/(?P<district>\d+)/(?P<gmina>[^\/]+)/(?P<circuit>[^\/]+)/$',
        views.circuit),
    url(r'^Polska/(?P<voivodeship>(?:\w|-)+)/(?P<district>\d+)/(?P<gmina>[^\/]+)/(?P<circuit>[^\/]+)/upload/$',
        views.upload),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^search_results/', views.search_results),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
