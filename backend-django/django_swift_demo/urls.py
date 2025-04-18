"""
URL configuration for django_swift_demo project.

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
from django.urls import path, include
from django.http import HttpResponse  # Import HttpResponse for a simple view
from api_test.views import test_api  # Import the test_api view function

# Define a simple view function
def home(request):
    return HttpResponse("Welcome to the Django Swift Demo!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/test/', test_api, name='test_api'),  # Add the API route# Add a route for the home page
    path('', include('api_test.urls')),  # Include app URLs
]