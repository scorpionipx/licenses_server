"""
URL configuration for licenses_server project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from licenses_server import views as licenses_server_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        '',
        licenses_server_views.HomePageView.as_view(),
        name='home',
    ),

    path(
        r'licenses/',
        include(
            ('licenses.model_based_urls.license', 'licenses'),
            namespace='licenses'
        ),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

