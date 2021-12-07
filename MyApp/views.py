from django.shortcuts import render, redirect
from MyApp.forms import PatientUserInfo, PatientSignUpForm, DoctorUserInfo, DoctorSignUpForm, AdminUserInfo, AdminSignUpForm, PatientAppointmentForm
from MyApp.models import Patient, Doctor, Appointment, PatientDischarge

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from datetime import date



#-------------------------------- MAIN PAGE VIEWS ----------------------------------
#-----------------------------------------------------------------------------------

def home(request):
    return render(request, 'MyApp/home.html')

def about(request):
    return render(request, 'MyApp/about.html')

def CentersofExcellence(request):
    return render(request, 'MyApp/CentersofExcellence.html')

def home_book_appointment(request):
    return render(request, 'MyApp/home_book_appointment.html')

def CovidTesting(request):
    return render(request, 'MyApp/CovidTesting.html')

def Covid19(request):
    return render(request,"MyApp/Covid19.html")

def CovidVaccination(request):
    return render(request,"MyApp/CovidVaccination.html")

def CovidResources(request):
    return render(request,"MyApp/CovidResources.html")
    
def Covid19Treatment(request):
    return render(request,"MyApp/Covid19Treatment.html")

def Covid19VaccineMyths(request):
    return render(request,"MyApp/Covid19VaccineMyths.html")

def Covid19Symptoms(request):
    return render(request,"MyApp/Covid19Symptoms.html")

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('MyApp:admin_dashboard')
    elif is_doctor(request.user):
        accountapproval=Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('MyApp:doctor_dashboard')
        else:
            return render(request,'MyApp/wait_approval.html')
    elif is_patient(request.user):
        accountapproval=Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('MyApp:patient_dashboard')
        else:
            return render(request,'MyApp/wait_approval.html')

#------------------------ PATIENT RELATED VIEWS START ------------------------------
#-----------------------------------------------------------------------------------

@login_required
def patient_dashboard(request):
    appointments=Appointment.objects.all().filter(patientId=request.user.id).order_by('-id')[:1]
    appointment=Appointment.objects.all().filter(patientId=request.user.id).count()
    print(appointment)
    if appointment!=0:
        status=appointments[0].status
        if status==True:
            doctorID=appointments[0].get_docId
            doctors=Doctor.objects.all().get(user_id=doctorID)
            mydict={
            'doctorName':appointments[0].doctorName,
            'doctorcontact':doctors.contact,
            'symptoms':appointments[0].description,
            'admitDate':appointments[0].appointmentDate,
            }
    else:
        print("hey")
        mydict={
        'doctorName':"Not assigned",
        'doctorcontact':"Not assigned",
        'symptoms':"Not assigned",
        'admitDate':"Not assigned",  
        }
    return render (request, 'MyApp/patient_dashboard.html',context=mydict)

@login_required
def patient_invoice(request):
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=PatientDischarge.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.contact,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'MyApp/Patient_Invoice.html',context=patientDict)

@login_required
def patient_book_appointment(request):
    appointmentForm=PatientAppointmentForm()
    patient=Patient.objects.get(user_id=request.user.id) 
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}

    if request.method=='POST':
        appointmentForm=PatientAppointmentForm(request.POST)

        if appointmentForm.is_valid():

            description=request.POST.get('description')
            doctor=Doctor.objects.get(user_id=request.POST.get('doctorId'))
            appointment=appointmentForm.save(commit=False)            
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=User.objects.get(id=request.POST.get('doctorId'))
            appointment.patientName=patient.get_name
            patient.assignedDoctorId=appointment.get_docId
            patient.symptoms=appointment.get_description
            appointment.status=False
            patient.save()
            appointment.save()

            return HttpResponseRedirect(reverse('MyApp:patient_my_appointment'))
        else:
                print(appointmentForm.errors)
        
    else: #no POST yet
        appointmentForm = PatientAppointmentForm()
    return render(request,'MyApp/patient_book_appointment.html',context=mydict)

@login_required
def patient_my_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id)
    appointments=Appointment.objects.all().filter(patientId=request.user.id)
    return render (request, 'MyApp/patient_my_appointment.html', {'appointments':appointments,'patient':patient})

@login_required
def wait_approval(request):
    return render (request, 'MyApp/wait_approval.html')

def PatientSignUp(request):
    registered = False

    if request.method == "POST":
        user_form = PatientUserInfo(data=request.POST)
        patient_form = PatientSignUpForm(data=request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            patientForm = patient_form.save(commit=False)
            patientForm.user = user
            patientForm.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            registered=True
            return redirect('MyApp:patientlogin')

        else:
                print(user_form.errors, patient_form.errors)
        
    else: #no POST yet
        user_form = PatientUserInfo()
        patient_form = PatientSignUpForm()
    
    return render(request, "MyApp/patientsignup.html", 
        {'user_form':user_form, 'patient_form': patient_form,'registered':registered})

def PatientLogin(request):
    if request.method=="POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)
        
        if user:
            if user.is_active:
                login(request, user) #login is the django's default function
                
                return HttpResponseRedirect(reverse('MyApp:afterlogin_view'))

            else: 
                return HttpResponse("Account not Active")
        
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied!")

    else:
        return render(request, 'MyApp/patientlogin.html',{})

#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#-----------------------------------------------------------------------------------


@login_required
def doctor_dashboard(request):
    doctor=Doctor.objects.get(user_id=request.user.id) 
    patientcount=Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=PatientDischarge.objects.all().distinct().filter(assignedDoctorName=doctor.get_name).count()
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    }
    return render (request, 'MyApp/doctor_dashboard.html',context=mydict)

@login_required
def doctor_wait_approval(request):
    return render (request, 'MyApp/doctor_wait_approval.html')

@login_required
def doctor_patient(request):
    mydict={
    'doctor':Doctor.objects.get(user_id=request.user.id), 
    }
    return render(request,'MyApp/doctor_patient.html',context=mydict)

@login_required
def doctor_view_patient(request):
    patients=Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor=Doctor.objects.get(user_id=request.user.id) 
    return render(request,'MyApp/doctor_view_patient.html',{'patients':patients,'doctor':doctor})

@login_required
def doctor_view_discharged_patient(request):
    doctor=Doctor.objects.get(user_id=request.user.id)
    dischargedpatients=PatientDischarge.objects.all().distinct().filter(assignedDoctorName=doctor.get_name)
    return render(request,'MyApp/doctor_view_discharged_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})


@login_required
def doctor_appointment(request):
    return render (request, 'MyApp/doctor_appointment.html')

@login_required
def doctor_view_appointment(request):
    doctor=Doctor.objects.get(user_id=request.user.id) 
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'MyApp/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})


@login_required
def doctor_delete_appointment(request):
    doctor=Doctor.objects.get(user_id=request.user.id) 
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'MyApp/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
def delete_appointment(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'MyApp/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})


def DoctorSignUp(request):
    registered = False

    if request.method == "POST":
        user_form = DoctorUserInfo(data=request.POST)
        doctor_form = DoctorSignUpForm(data=request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctorForm = doctor_form.save(commit=False)
            doctorForm.user = user
            doctorForm.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            registered=True
            return redirect('MyApp:doctorlogin')

        else:
                print(user_form.errors, doctor_form.errors)
        
    else: #no POST yet
        user_form = DoctorUserInfo()
        doctor_form = DoctorSignUpForm()
    
    return render(request, "MyApp/doctorsignup.html", 
        {'user_form':user_form, 'doctor_form': doctor_form, 'registered':registered})

def DoctorLogin(request):
    if request.method=="POST":
        username = request.POST.get('username') #name from the html input is passed in brackets
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)
        
        if user:
            if user.is_active:
                login(request, user) #login is the django's default function
                
                return HttpResponseRedirect(reverse('MyApp:afterlogin_view'))

            else: 
                return HttpResponse("Account not Active")
        
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied!")

    else:
        return render(request, 'MyApp/doctorlogin.html',{})


#--------------------------------- LOGOUT VIEW ------------------------------------
#-----------------------------------------------------------------------------------

def logout_view(request):
    logout(request)
    return redirect('home')

#_____________________________ ADMIN RELATED VIEWS START ____________________________________________________


def AdminSignUp(request):
    registered = False

    if request.method == "POST":
        admin_form = AdminUserInfo(data=request.POST)
        
        if admin_form.is_valid():
            user = admin_form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            registered=True
            return redirect('MyApp:adminlogin')

        else:
                print(admin_form.errors)
        
    else: #no POST yet
        admin_form = AdminSignUpForm()
    
    return render(request, "MyApp/adminsignup.html", 
        {'admin_form':admin_form,'registered':registered})

def AdminLogin(request):
    if request.method=="POST":
        username = request.POST.get('username') #name from the html input is passed in brackets
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)
        
        if user:
            if user.is_active:
                login(request, user) #login is the django's default function
                
                return HttpResponseRedirect(reverse('MyApp:admin_dashboard'))

            else: 
                return HttpResponse("Account not Active")
        
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied!")

    else:
        return render(request, 'MyApp/adminlogin.html',{})

@login_required(login_url='adminlogin')
def admin_dashboard(request):
    #for both table in admin dashboard
    doctors=Doctor.objects.all().order_by('-id')
    patients=Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=Doctor.objects.all().filter(status=False).count()

    patientcount=Patient.objects.all().filter(status=True).count()
    pendingpatientcount=Patient.objects.all().filter(status=False).count()

    appointmentcount=Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'MyApp/admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_patient(request):
    return render (request, 'MyApp/admin_patient.html')

@login_required(login_url='adminlogin')
def admin_doctor(request):
    return render (request, 'MyApp/admin_doctor.html')

@login_required(login_url='adminlogin')
def admin_appointment(request):
    return render (request, 'MyApp/admin_appointment.html')
    
# _______________________________________________________________________________________________________

@login_required(login_url='adminlogin')
def admin_patient_record(request):
    patients=Patient.objects.all().filter(status=True)
    return render(request,'MyApp/admin_patient_record.html',{'patients':patients})

@login_required(login_url='adminlogin')
def delete_patient(request, pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('MyApp:admin_patient_record')


@login_required(login_url='adminlogin')
def update_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    userForm=PatientUserInfo(instance=user)
    patientForm=PatientSignUpForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserInfo(request.POST,instance=user)
        patientForm=PatientSignUpForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            print("Hi")
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            #patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('MyApp:admin_patient_record')
        else:
                print(userForm.errors, patientForm.errors)
        
    else: #no POST yet
        userForm = PatientUserInfo()
        patientForm = PatientSignUpForm()
    return render(request,'MyApp/admin_update_patient.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_admit_patient(request):
    userForm=PatientUserInfo()
    patientForm=PatientSignUpForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserInfo(request.POST)
        patientForm=PatientSignUpForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            return HttpResponseRedirect('admin_patient_record')
        else:
                print(userForm.errors, patientForm.errors)
        
    else: #no POST yet
        userForm = PatientUserInfo()
        patientForm = PatientSignUpForm()

    return render(request,'MyApp/admin_admit_patient.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_patient(request):
    #those whose approval are needed
    patients=Patient.objects.all().filter(status=False)
    return render(request,'MyApp/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
def approve_patient(request, pk):
    patient=Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('MyApp:admin_approve_patient'))

@login_required(login_url='adminlogin')
def admin_discharge_patient(request):
    patients=Patient.objects.all().filter(status=True)
    return render(request,'MyApp/admin_discharge_patient.html',{'patients':patients})

@login_required(login_url='adminlogin')
def discharge_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=Doctor.objects.get(user_id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'contact':patient.contact,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':"Dr. "+assignedDoctor.get_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (PatDisc)
        PatDisc=PatientDischarge()
        PatDisc.patientId=pk
        PatDisc.patientName=patient.get_name
        PatDisc.assignedDoctorName=assignedDoctor.get_name
        PatDisc.address=patient.address
        PatDisc.mobile=patient.contact
        PatDisc.symptoms=patient.symptoms
        PatDisc.admitDate=patient.admitDate
        PatDisc.releaseDate=date.today()
        PatDisc.daySpent=int(d)
        PatDisc.medicineCost=int(request.POST['medicineCost'])
        PatDisc.roomCharge=int(request.POST['roomCharge'])*int(d)
        PatDisc.doctorFee=int(request.POST['doctorFee'])
        PatDisc.OtherCharge=int(request.POST['OtherCharge'])
        PatDisc.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        PatDisc.save()
        return render(request,'MyApp/patient_final_bill.html',context=patientDict)
    return render(request,'MyApp/patient_generate_bill.html',context=patientDict)


@login_required(login_url='adminlogin')
def reject_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('MyApp:admin_approve_patient')

# _______________________________________________________________________________________________________

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf(request,pk):
    dischargeDetails=PatientDischarge.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('MyApp/download_bill.html',dict)
# _______________________________________________________________________________________________________

@login_required(login_url='adminlogin')
def admin_doctor_record(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'MyApp/admin_doctor_record.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
def delete_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('MyApp:admin_doctor_record')

@login_required(login_url='adminlogin')
def update_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.user_id)
    userForm=DoctorUserInfo(instance=user)
    doctorForm=DoctorSignUpForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=DoctorUserInfo(request.POST,instance=user)
        doctorForm=DoctorSignUpForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            print("Hi")
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('MyApp:admin_doctor_record')
        else:
                print(userForm.errors, doctorForm.errors)
        
    else: #no POST yet
        userForm = DoctorUserInfo()
        doctorForm = DoctorSignUpForm()
    return render(request,'MyApp/admin_update_doctor.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_add_doctor(request):
    userForm=DoctorUserInfo()
    doctorForm=DoctorSignUpForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=DoctorUserInfo(request.POST)
        doctorForm=DoctorSignUpForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='PATIENT')
            my_doctor_group[0].user_set.add(user)
            return HttpResponseRedirect('admin_doctor_record')
        else:
                print(userForm.errors, doctorForm.errors)
        
    else: #no POST yet
        userForm = DoctorUserInfo()
        doctorForm = DoctorSignUpForm()

    return render(request,'MyApp/admin_add_doctor.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_approve_doctor(request):
    #those whose approval are needed
    doctors=Doctor.objects.all().filter(status=False)
    return render(request,'MyApp/admin_approve_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
def approve_doctor(request, pk):
    doctor=Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('MyApp:admin_approve_doctor'))

@login_required(login_url='adminlogin')
def reject_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('MyApp:admin_approve_doctor')

@login_required(login_url='adminlogin')
def admin_doctor_specialization(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'MyApp/admin_doctor_specialization.html',{'doctors':doctors})
 
# _________________________________________________________________________________________________

@login_required(login_url='adminlogin')
def admin_appointment_view(request):
    return render(request,'MyApp/admin_appointment.html')

@login_required(login_url='adminlogin')
def admin_view_appointment(request):
    appointments=Appointment.objects.all().filter(status=True)
    return render(request,'MyApp/admin_view_appointment.html',{'appointments':appointments})

@login_required(login_url='adminlogin')
def admin_add_appointment(request):
    appointmentForm=PatientAppointmentForm()
    mydict={'appointmentForm':appointmentForm}

    if request.method=='POST':
        appointmentForm=PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
            return HttpResponseRedirect('admin_view_appointment')
        else:
            print(appointmentForm.errors)
        
    else: #no POST yet
        appointmentForm = PatientAppointmentForm()
    return render(request,'MyApp/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
def admin_approve_appointment(request):
    appointments=Appointment.objects.all().filter(status=False)
    return render(request,'MyApp/admin_approve_appointment.html',{'appointments':appointments})


@login_required(login_url='adminlogin')
def approve_appointment(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('MyApp:admin_approve_appointment'))



@login_required(login_url='adminlogin')
def reject_appointment(request,pk):
    appointment=Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('MyApp:admin_approve_appointment')