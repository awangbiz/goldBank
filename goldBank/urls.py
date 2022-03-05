"""goldBank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

# drf_yasg code starts here
from django.conf import settings #awang needed for static url
from django.conf.urls.static import static #awang needed for static url
from django.urls import  re_path 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Account Management",
        default_version='1.0',
        description="TM Account Mamnagement API",
        # terms_of_service="https://www.",
        # contact=openapi.Contact(email="jason@jaseci.org"),
        # license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [
    #  drf_yasg code starts here
    re_path(r'^doc(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),  #<-- Here
    path('docs', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),  #<-- Here
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  #<-- Here
    # drf_yasg code ends here

    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]+ static(settings.STATIC_URL)