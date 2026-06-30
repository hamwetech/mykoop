"""
URL configuration for bkkfarmer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static

from conf.views import upload_locations
from system.views import DashboardView

def redirect_admin(request):
    return redirect('/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    path("upload-locations/", upload_locations, name="upload_locations"),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    path('payments/', include('payments.urls')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('', include('system.urls')),
    path('', include('conf.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
