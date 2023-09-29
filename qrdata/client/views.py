from django.shortcuts import render,redirect
from client.models import client,clientinfo,clientdocument
import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from client.utils import render_to_pdf

# Create your views here.
def index(request):
    return render(request,"index.html")
def base(request):
    return render(request,"base.html")
def signup(request):
    return render(request,"signup.html")
def login(request):
    return render(request,"login.html")
def clientregister(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        photo=request.FILES['photo']
        client_obj=client(username=username,email=email,password=password,photo=photo)
        error_msg=validate(client_obj)
        if not error_msg:
            client_obj.save()
            return redirect("adminchk")
    return render(request,"signup.html",{'error':error_msg})
def validate(client_obj):
     error_msg=None
     mail=client.objects.filter(email=client_obj.email)
     if mail:
          error_msg="E-mail already exist"
     return error_msg
def adminchk(request):
    return render(request,"adminchk.html")
def clientlogin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        try:
            
                client_obj=client.objects.get(email=email)
            
        except:
            error_msg="client does not exist"
            return render(request,"signup.html",{'error1':error_msg})
        data={'obj': client_obj}
        print("obj=",data)
        if client_obj and client_obj.status==1:
                  print("object ok")
                  
                  if(password==client_obj.password):
                    print("success")
                       
                    request.session['id']=client_obj.id
                    request.session['name']=client_obj.username
                    return render(request,"clienthome.html",data)
    return render(request,"signup.html")
def clienthome(request):
    return render(request,"clienthome.html")
def clientdata(request):
     if request.method=="POST":
          phone=request.POST.get("phone")
          dob=request.POST.get("dob")
          aadhar=request.POST.get("aadhar")
          street=request.POST.get("street")
          country=request.POST.get("country")
          city=request.POST.get("city")
          print(phone,dob,aadhar,street,country,city,request.session['id'])
                        
          obj=clientinfo(phone=phone,dob=dob,aadhar=aadhar,street=street,country=country,city=city,Client=client(request.session['id']))
          obj.save()
          #qrcode
          document=clientdocument(Client=clientinfo(obj.id))
          clientobj=client.objects.get(id=request.session['id'])
          print(clientobj.email)
          today_date=datetime.date.today()
          name=clientobj.username
          email=clientobj.email
          
          img=qrcode.make("QR Code Created Date:%s \n\n Name:'%s' \n\n Email Address:'%s' \n\n Contact NO:'%s' \n\n DOB:'%s' ' \n\n Address:'%s' \n\n Country:'%s' \n\n City:'%s'  \n\n Aadhar No:'%s'"%(str(today_date),str(name),str(email),str(phone),str(dob),str(street),str(country),str(city),str(aadhar)))
          imgfile="img%s.jpg"%(obj.id)
          img.save(imgfile)
          buffer=BytesIO()
          img.save(buffer,'PNG')
          document.qrdata.save(imgfile,File(buffer))
          #pdf
          global pdf
          pdf=render_to_pdf(obj.id,'certificate.html',{'clientobj':clientobj,'obj':obj})
          #document=clientdocument(Client=clientinfo(obj.id))
          global filename
          filename="doc%s.pdf"%(obj.id)
          document.pdfdata.save(filename,File(BytesIO(pdf.content)))
          document.save()

          return render(request,"result.html",{'document':document})
            
          
              
          #print("obj=",obj)
          #obj.save()
     return render(request,"clientdata.html")
def logoutclient(request):
               
               request.session.clear()
               return redirect('/')
    