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
from django.contrib.auth import views as auth_views
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
    path('Thankyou', views.thankyou, name='Thankyou'),

    path('Register', views.register, name='register'),
    path('Login', views.Login, name='login'),
    path('Logout', views.Logout, name='logout'),

# PASSWORD
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name='password_reset_complete'),

    path('export_csv', views.export_csv, name='export-csv'),
    path('export_xls', views.export_xls, name='export-xls'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
