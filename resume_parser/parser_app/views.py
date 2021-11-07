from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import ListView
from pyresparser import ResumeParser
from .models import *
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
import os
import csv
import xlwt
import datetime

from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .decorators import unauthenticated_user

def validate(customer):
    if customer.Subscription == True:
        customer.Number_of_Resumes = customer.Number_of_Resumes + 1
        customer.save()
        return True

    if customer.Number_of_Resumes < 3:
        customer.Number_of_Resumes = customer.Number_of_Resumes + 1
        customer.save()
        return True
    else:
        return False



def Parser(request):

    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        value = validate(customer)
        if value == False:
            return render(request, 'pricing.html', )
        Resume.objects.all().delete()
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.getlist('resume')
        resumes_data = []
        if file_form.is_valid():
            for file in files:
                try:
                    # saving the file
                    resume = Resume(resume=file)
                    resume.save()

                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    resumes_data.append(data)
                    resume.name = data.get('name')
                    resume.email = data.get('email')
                    resume.mobile_number = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education = ', '.join(data.get('degree'))
                    else:
                        resume.education = None
                    resume.company_names = data.get('company_names')
                    resume.college_name = data.get('college_name')
                    resume.designation = data.get('designation')
                    resume.total_experience = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills = ', '.join(data.get('skills'))
                    else:
                        resume.skills = None
                    if data.get('experience') is not None:
                        resume.experience = ', '.join(data.get('experience'))
                    else:
                        resume.experience = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
            resumes = Resume.objects.all()
            messages.success(request, 'Resumes uploaded!')
            context = {
                'resumes': resumes,
            }
            return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Parsed' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(
        ['name', 'email', 'mobile_number', 'degree', 'company_names', 'college_name', 'designation', 'total_experience',
         'skills', 'experience'])

    resume = Resume.objects.all().values_list('name', 'email', 'mobile_number', 'education', 'company_name',
                                              'college_name', 'designation', 'total_experience', 'skills', 'experience')
    for r in resume:
        writer.writerow(r)
    return response


def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Parsed' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parsed Data')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['name', 'email', 'mobile_number', 'degree', 'company_names', 'college_name', 'designation',
               'total_experience', 'skills', 'experience']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Resume.objects.all().values_list('name', 'email', 'mobile_number', 'education', 'company_name',
                                            'college_name', 'designation', 'total_experience', 'skills', 'experience')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def index(request):
    return render(request, 'index.html', )


def about(request):
    return render(request, 'about.html', )


def pricing(request):
    return render(request, 'pricing.html', )

def payment_form(request):
    return render(request, 'payment_form.html', )

def payment(request):
    customer = Customer.objects.get(user=request.user)
    if customer:
        customer.Subscription = bool(True)
        customer.save()
        return redirect('homepage')


def service(request):
    return render(request, 'service.html', )


def project(request):
    return render(request, 'project.html', )


def contact(request):
    return render(request, 'contact.html', )

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("homepage")
    else:
        form = NewUserForm()
    return render(request, 'Register.html', {'form': form})

@unauthenticated_user
def Login(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'Login.html', {'login_form': form})

def Logout(request):
    logout(request)
    messages.success(request, 'you are logged out')
    return redirect('homepage')

