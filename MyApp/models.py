from django.db import models
from django.contrib.auth.models import User

#__________________________________________________________________________________________________________________________________

GENDER =[
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]
Time = [
    ("10:00 A.M","10:00 A.M"),
    ("10:30 A.M","10:30 A.M"),
    ("11:00 A.M","11:00 A.M"),
    ("11:30 A.M","11:30 A.M"),
    ("12:00 P.M","12:00 P.M"),
    ("12:30 P.M","12:30 P.M"),
    ("01:00 P.M","01:00 P.M"),
    ("01:30 P.M","01:30 P.M"),
    ("05:00 P.M","05:00 P.M"),
    ("05:30 P.M","05:30 P.M"),
    ("06:00 P.M","06:00 P.M"),
    ("06:30 P.M","06:30 P.M"),
    ("07:00 P.M","07:00 P.M"),
    ("07:30 P.M","07:30 P.M"),
    ("08:00 P.M","08:00 P.M"),
    ("08:30 P.M","08:30 P.M"),
]

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Patient_First_Name = models.CharField(max_length=50, default="")
    Patient_Last_Name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=10, choices=GENDER)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=350)
    symptoms = models.CharField(max_length=500, default="")
    status = models.BooleanField(default=False)                        
    admitDate = models.DateField(auto_now=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)  


    @property
    def get_name(self):
        return self.Patient_First_Name+" "+self.Patient_Last_Name

    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return self.Patient_First_Name+" "+self.Patient_Last_Name
    
#__________________________________________________________________________________________________________________________________


departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('General Physician','General Physician'),
('NeuroSurgeon','NeuroSurgeon'),
('GastroEntologists','GastroEntologists'),
('Pediatrician','Pediatrician'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Doctor_First_Name = models.CharField(max_length=50, default="")
    Doctor_Last_Name = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=10, choices=GENDER,default="")
    address = models.CharField(max_length=40)
    contact = models.CharField(max_length=10,null=True)
    department= models.CharField(max_length=50,choices=departments,default='')
    status = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.Doctor_First_Name+" "+self.Doctor_Last_Name
    
    @property
    def get_id(self):
        return self.id

    def __str__(self):
        return "{} ({})".format(self.Doctor_First_Name+" "+self.Doctor_Last_Name,self.department)

#__________________________________________________________________________________________________________________________________
        
class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(null=False)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    time = models.CharField(max_length=10, choices=Time,default="")

    @property
    def get_docId(self):
        return self.doctorId

    @property
    def get_description(self):
        return self.description

    @property
    def get_status(self):
        return self.status

#__________________________________________________________________________________________________________________________________


class PatientDischarge(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)
    roomCharge=models.PositiveIntegerField(null=False, default=0)
    medicineCost=models.PositiveIntegerField(null=False,default=0)
    doctorFee=models.PositiveIntegerField(null=False, default=0)
    OtherCharge=models.PositiveIntegerField(null=False, default=0)
    total=models.PositiveIntegerField(null=False)


#__________________________________________________________________________________________________________________________________
#________________________________________________________________________________________________________________________
