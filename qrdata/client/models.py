from django.db import models
import datetime

# Create your models here.
class client(models.Model):
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    photo=models.ImageField(upload_to="client_data")
    status=models.BooleanField(default=False)
class clientinfo(models.Model):
    phone=models.CharField(max_length=20)
    dob=models.DateField(null=True,blank=True,default=None)
    aadhar=models.CharField(max_length=15)
    street=models.CharField(max_length=15)
    country=models.CharField(max_length=15)
    city=models.CharField(max_length=15)
    Client=models.ForeignKey(client,on_delete=models.CASCADE)
class clientdocument(models.Model):
    pdfdata=models.FileField(upload_to="documents",null=True,blank=True)
    qrdata=models.ImageField(upload_to="qrcode",null=True,blank=True)
    Client=models.ForeignKey(clientinfo,on_delete=models.CASCADE)    
    

