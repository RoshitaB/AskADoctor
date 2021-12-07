from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from MyApp import views
from django.contrib.auth.views import LoginView,LogoutView

app_name="MyApp"

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('afterlogin_view/', views.afterlogin_view, name="afterlogin_view"),
    path('Covid19/', views.Covid19, name="Covid19"),
    path('CentersofExcellence/', views.CentersofExcellence, name="CentersofExcellence"),
    path('home_book_appointment/', views.home_book_appointment, name="home_book_appointment"),
    path('CovidTesting/', views.CovidTesting, name="CovidTesting"),
    path('CovidVaccination/', views.CovidVaccination, name="CovidVaccination"),
    path('CovidResources/', views.CovidResources, name="CovidResources"),
    path('Covid19Treatment/', views.Covid19Treatment, name="Covid19Treatment"),
    path('Covid19VaccineMyths/', views.Covid19VaccineMyths, name="Covid19VaccineMyths"),
    path('Covid19Symptoms/', views.Covid19Symptoms, name="Covid19Symptoms"),
    path('logout/', LogoutView.as_view(template_name='MyApp/home.html'),name='logout'),


    path('patientlogin/', views.PatientLogin, name="patientlogin"),
    path('patientsignup/', views.PatientSignUp, name="patientsignup"),
    path('patient_dashboard/', views.patient_dashboard, name="patient_dashboard"),
    path('patient_book_appointment/', views.patient_book_appointment, name="patient_book_appointment"),
    path('patient_my_appointment/', views.patient_my_appointment, name="patient_my_appointment"),
    path('patient_invoice/', views.patient_invoice, name="patient_invoice"),
    path('wait_approval/', views.wait_approval, name="wait_approval"), 


    path('doctorlogin/', views.DoctorLogin, name="doctorlogin"),
    path('doctorsignup/', views.DoctorSignUp, name="doctorsignup"),
    path('doctor_dashboard/', views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor_wait_approval/', views.doctor_wait_approval, name="doctor_wait_approval"),
    path('doctor_patient/', views.doctor_patient, name="doctor_patient"),  
    path('doctor_appointment/', views.doctor_appointment, name="doctor_appointment"),
    path('doctor_view_patient/', views.doctor_view_patient, name="doctor_view_patient"),
    path('doctor_view_discharged_patient/', views.doctor_view_discharged_patient, name="doctor_view_discharged_patient"), 
    path('doctor_view_appointment/', views.doctor_view_appointment, name="doctor_view_appointment"),
    path('doctor_delete_appointment/', views.doctor_delete_appointment, name="doctor_delete_appointment"),


    path('adminlogin/', views.AdminLogin, name="adminlogin"),
    path('adminsignup/', views.AdminSignUp, name="adminsignup"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_patient/', views.admin_patient, name="admin_patient"),
    path('admin_patient_record/', views.admin_patient_record, name="admin_patient_record"),
    path('admin_admit_patient/', views.admin_admit_patient, name="admin_admit_patient"),    
    path('admin_approve_patient/', views.admin_approve_patient,name="admin_approve_patient"),
    path('admin_discharge_patient/', views.admin_discharge_patient,name='admin_discharge_patient'),
    path('approve_patient/<int:pk>', views.approve_patient,name='approve_patient'),
    path('reject_patient/<int:pk>', views.reject_patient,name='reject_patient'),
    path('update_patient/<int:pk>', views.update_patient,name='update_patient'),
    path('delete_patient/<int:pk>', views.delete_patient,name='delete_patient'),
    path('discharge_patient/<int:pk>', views.discharge_patient,name='discharge_patient'),
    path('download_pdf/<int:pk>', views.download_pdf,name='download_pdf'),

    path('admin_doctor/', views.admin_doctor, name="admin_doctor"),
    path('admin_doctor_record/', views.admin_doctor_record,name="admin_doctor_record"),
    path('admin_add_doctor/', views.admin_add_doctor,name="admin_add_doctor"),
    path('admin_approve_doctor/', views.admin_approve_doctor,name="admin_approve_doctor"),
    path('admin_doctor_specialization/', views.admin_doctor_specialization,name="admin_doctor_specialization"),
    path('update_doctor/<int:pk>', views.update_doctor,name='update_doctor'),
    path('delete_doctor/<int:pk>', views.delete_doctor,name='delete_doctor'),
    path('approve_doctor/<int:pk>', views.approve_doctor,name='approve_doctor'),
    path('reject_doctor/<int:pk>', views.reject_doctor,name='reject_doctor'),

    path('admin_appointment/', views.admin_appointment, name="admin_appointment"),
    path('admin_view_appointment/', views.admin_view_appointment, name="admin_view_appointment"),
    path('admin_add_appointment/', views.admin_add_appointment, name="admin_add_appointment"),
    path('admin_approve_appointment/', views.admin_approve_appointment, name="admin_approve_appointment"),
    path('approve_appointment/<int:pk>', views.approve_appointment,name='approve_appointment'),
    path('reject_appointment/<int:pk>', views.reject_appointment,name='reject_appointment'),
    path('delete_appointment/<int:pk>', views.delete_appointment,name='delete_appointment'),
]