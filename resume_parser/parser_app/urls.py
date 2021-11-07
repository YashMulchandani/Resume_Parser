"""resume_parser.parser_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='homepage'),
    path('Parser', views.Parser, name='Parser'),
    path('About', views.about, name='about'),
    path('Pricing', views.pricing, name='pricing'),
    path('Payment_form', views.payment_form, name='payment_form'),
    path('Payment', views.payment, name='payment'),
    path('Service', views.service, name='service'),
    path('Project', views.project, name='project'),
    path('Contact', views.contact, name='contact'),

    path('Register', views.register, name='register'),
    path('Login', views.Login, name='login'),
    path('Logout', views.Logout, name='logout'),

    path('export_csv', views.export_csv, name='export-csv'),
    path('export_xls', views.export_xls, name='export-xls'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
