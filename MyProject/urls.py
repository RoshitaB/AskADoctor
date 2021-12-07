"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from MyApp import views

app_name="MyApp"

urlpatterns = [
    path('', include('MyApp.urls')),
    path('home/', include('MyApp.urls')),
    path('about/', include('MyApp.urls')),
    path('afterlogin_view/', include('MyApp.urls')),
    path('Covid19/', include('MyApp.urls')),
    path('CentersofExcellence/', include('MyApp.urls')),
    path('home_book_appointment/', include('MyApp.urls')),
    path('CovidTesting/', include('MyApp.urls')),
    path('CovidVaccination/', include('MyApp.urls')),
    path('CovidResources/', include('MyApp.urls')),
    path('Covid19Treatment/', include('MyApp.urls')),
    path('Covid19VaccineMyths/', include('MyApp.urls')),
    path('Covid19Symptoms/', include('MyApp.urls')),
    path('logout/', include('MyApp.urls')),


    path('patientlogin/', include('MyApp.urls')),
    path('patientsignup/', include('MyApp.urls')),
    path('patient_dashboard/', include('MyApp.urls')),
    path('patient_book_appointment/', include('MyApp.urls')),
    path('patient_my_appointment/', include('MyApp.urls')),
    path("patient_invoice/", include('MyApp.urls')),
    path("patient_covid19/", include('MyApp.urls')),
    path("wait_approval/", include('MyApp.urls')),


    path('doctorlogin/', include('MyApp.urls')),
    path('doctorsignup/', include('MyApp.urls')),
    path('doctor_dashboard/', include('MyApp.urls')),
    path("doctor_wait_approval/", include('MyApp.urls')),
    path("doctor_patient/", include('MyApp.urls')),
    path("doctor_patient/", include('MyApp.urls')),
    path("doctor_appointment/", include('MyApp.urls')),
    path("doctor_view_patient/", include('MyApp.urls')),
    path("doctor_view_discharged_patient/", include('MyApp.urls')),
    path('doctor_view_appointment/', include('MyApp.urls')),
    path('doctor_delete_appointment/', include('MyApp.urls')),


    path('adminlogin/', include('MyApp.urls')),
    path('adminsignup/', include('MyApp.urls')),
    path('admin_dashboard/', include('MyApp.urls')),
    path('admin_patient/', include('MyApp.urls')),
    path('admin_patient_record/', include('MyApp.urls')),
    path('admin_admit_patient/', include('MyApp.urls')),
    path('admin_approve_patient/', include('MyApp.urls')),
    path('approve_patient/<int:pk>', include('MyApp.urls')),
    path('admin_discharge_patient/', include('MyApp.urls')),
    path('discharge_patient/', include('MyApp.urls')),
    path('admin_appointment/', include('MyApp.urls')),
    path('update_patient/<int:pk>', include('MyApp.urls')),
    path('delete_patient/', include('MyApp.urls')),
    path('download_pdf/<int:pk>', include('MyApp.urls')),

    path('admin_doctor/', include('MyApp.urls')),
    path('admin_doctor_record/', include('MyApp.urls')),
    path('admin_add_doctor/', include('MyApp.urls')),
    path('admin_approve_doctor/', include('MyApp.urls')),
    path('approve_doctor/<int:pk>', include('MyApp.urls')),
    path('reject_doctor/<int:pk>', include('MyApp.urls')),
    path('admin_doctor_specialization/', include('MyApp.urls')),    
    path('update_doctor/<int:pk>', include('MyApp.urls')),
    path('delete_doctor/', include('MyApp.urls')),
    
    path('admin_appointment/', include('MyApp.urls')),
    path('admin_view_appointment/', include('MyApp.urls')),
    path('admin_add_appointment/', include('MyApp.urls')),
    path('admin_approve_appointment/', include('MyApp.urls')),  
    path('approve_appointment/<int:pk>',include('MyApp.urls')),
    path('reject_appointment/<int:pk>', include('MyApp.urls')), 
    path('delete_appointment/<int:pk>', include('MyApp.urls')),  

    path('admin/', admin.site.urls),
]