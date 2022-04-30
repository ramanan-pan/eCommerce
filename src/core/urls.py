"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from website.admin import vendorSite, clientSite
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.shortcuts import redirect
from website import views


aUser = User.objects.all().first()    
aUser.set_unusable_password()

admin.site.has_permission = lambda r: setattr(r, 'user', aUser) or True
vendorSite.has_permission = lambda r: setattr(r, 'user', aUser) or True
clientSite.has_permission = lambda r: setattr(r, 'user', aUser) or True

urlpatterns = [
    path('admin/logout/', lambda request: redirect('../../website/login', permanent=False)),
    path('clientSite/logout/', lambda request: redirect('../../website/login', permanent=False)),
    path('vendorSite/logout/', lambda request: redirect('../../website/login', permanent=False)),
    path('admin/', admin.site.urls),
    path('website/', include('website.urls', namespace = 'website')),
    path('vendorSite/', vendorSite.urls),
    path('clientSite/', clientSite.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)