"""
URL configuration for snapexpress project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from api.views import *
from api.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('',home,name='home'),
    path("choose_template",choose_template,name='choose_template'),
    path("take_photo/<int:id>",take_photo,name='take_photo'),
    path("result",final_output,name='final_output'),
    path("gettemplates",gettemplates,name='gettemplates'),
    path("manage_events",manage_events,name='manage_events'),
    path("change_current_event",change_current_event,name='change_current_event'),
    path("fetch_event_images",fetch_event_images,name='fetch_event_images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
