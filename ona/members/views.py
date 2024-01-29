import datetime, os, math, random, requests, json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from .models import Member, Sub, Payment


# Create your views here.

def home(request):
    # template = loader.get_template('index.html')
    # # return HttpResponse(template.render())
    return render(request, 'index.html')

       
def members(request):
    userID=request.session['userid']
    if userID != None:
        mymember = Member.objects.all().values()
        template = loader.get_template('all_members.html')
        context = {'mymember': mymember, "userID":userID}
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('detail.html')
    context = {'mymember': mymember}
    return HttpResponse(template.render(context, request))


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
        

def subreg(request):
    if request.method =='POST':
        print(request.POST)
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        confirm_password = request.POST.get('cpwd')
        phone_number = request.POST.get('phone')
        context = {'firstname':firstname,
                   'lastname':lastname,
                   'email':email,
                   "password":password,
                   "confirm_password":confirm_password,
                   "phone":phone_number
                   }
        # print(context)
        if (firstname=="" or 
            lastname == "" or 
            email=="" or 
            password == "" or 
            confirm_password=="" or
            phone_number ==""):
            # template = loader.get_template('signup.html')
            messages.error(request, "Please fill all field")
            return render(request, 'signup.html', context=context)
        elif password != confirm_password:
            messages.error(request, "Password does not match")
            return render(request, 'signup.html', context=context)
        else:
            hashpass = make_password(password)
            mmd = Member.objects.create(firstname=firstname, 
                         lastname=lastname,
                         phone=phone_number,
                         email = email,
                         password = hashpass,
                         joined_date = datetime.datetime.now()
                         )
            mmd.save()
            messages.success(request, "Registration successful")
            # return render(request, 'login.html')
            return redirect('/login/')
            
    
def login(request):
    if request.method=='GET':
        return render(request, 'login.html')

def sub_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        
        if email == "" or pwd =="":
            messages.error(request, "One or more filed is empty")
            return redirect('/login/')
        else:
            try:
                user = Member.objects.get(email=email)         
                if user is not None:
                    passmatch = check_password(pwd, user.password)                   
                    if passmatch:
                        # request.session['userid'] = request.session.session_key
                        request.session['userid'] = user.id
                        # print(request.session['userid'])
                        messages.success(request, "Login successful")
                        return redirect(f'/dashboard/{user.id}/')
                    else:
                        messages.error(request, "Incorrect credentials")
                        return redirect('/login/')     
                else:
                    messages.error(request, "Record Not Found")
                    return redirect('/login/')
            except Member.DoesNotExist:
                messages.error(request, "user can not be found")
                return redirect('/login/')
            

def dashboard(request, id):
    try:
        userID = request.session['userid']
        actUser = Member.objects.get(id=id)
        mymember = Member.objects.all().values()
        sub = Sub.objects.get(sub_memberId=actUser, sub_status='active')
        context = {"user":actUser, "userID":userID, "sub":sub, "mymember":mymember}
        return render(request, 'dashboard.html', context)
    except Member.DoesNotExist:
        return redirect('/')

def editprofile(request):
    if request.method=='GET':
        try:
            userID = request.session['userid']
            actUser = Member.objects.get(id=userID)
            context = {"user":actUser, "userID":userID}
            return render(request, "editprofile.html", context)
        except Member.DoesNotExist:
            return redirect('/')
        
            
def sub_edit(request):
    if request.method=='POST':
        try:
            userID = request.session['userid']
            firstname = request.POST.get('fname')
            lastname = request.POST.get('lname')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            if (
                firstname !="" or
                lastname !="" or
                email !="" or
                phone !=""
            ):
                mmd = Member.objects.get(id=userID)
                mmd.firstname=firstname
                mmd.lastname=lastname
                mmd.email=email
                mmd.phone=phone
                mmd.save()
                messages.success(request, "Profile updated successfully")
                return redirect(f'/dashboard/{userID}/')
            else:
                messages.error(request, "Unable to update profile")
                return redirect(f'/dashboard/{userID}/')
        except Member.DoesNotExist:
            return redirect('/')
        

def upload(request, id):
    if request.method == 'POST':
        try:
            userID = request.session['userid']
            imgfile = request.FILES.get('pic')
            originalname = imgfile.name
            if originalname !="":
                extension = os.path.splitext(originalname)
                if extension[1].lower() in ['.jpg', '.gif', '.png', '.jpeg' ]:
                    fn=math.ceil(random.random()*10000000000)
                    saveas = str(fn) + extension[1]
                    save_path=(f'members/static/images/{saveas}')
                    with open(save_path, 'wb') as sp:
                        sp.write(imgfile.read())
                    dk = Member.objects.get(id=userID)
                    dk.pic = saveas
                    dk.save()
                    messages.success(request, "Uploaded successfully")
                    return redirect(f'/dashboard/{userID}/')
            else:
                messages.error(request, "Error uploading picture")
                return redirect(f'/dashboard/{userID}/')
        except Member.DoesNotExist:
            return redirect('/')    


def subscribe(request, id):
    if request.method == 'GET':
        try:
            userID = request.session['userid']
            context = {"userID":userID}
            return render (request, 'subscribe.html', context)
        except Member.DoesNotExist:
            return redirect(f"/dashboard/{userID}/")
            

def suborder(request, id):
    if request.method == 'POST':
        try:
            userID = request.session['userid']
            pp = request.POST.get('plan')
            ordercode = int(random.random()*10000000)
            request.session['refno'] = ordercode
            if pp == "":
                messages.error(request, "Order unsuccessful")
                return redirect(f"/dashboard/{userID}/subscribe/")
            else:
                usdid = Member.objects.get(id=id)
                if pp=='1000':
                    ord = Sub.objects.create(sub_type='Starter',
                                             sub_amount=pp,
                                             sub_date=datetime.datetime.now(),
                                             sub_status='pending',
                                             sub_memberId=usdid,
                                             sub_refno = ordercode)
                    ord.save()
                    messages.success(request, 'Order successful')
                    return redirect('/payment/')
                elif pp=='1500':
                    ord = Sub.objects.create(sub_type='Intermediate',
                                             sub_amount=pp,
                                             sub_date=datetime.datetime.now(),
                                             sub_status='pending',
                                             sub_memberId=usdid,
                                             sub_refno = ordercode)
                    ord.save()
                    messages.success(request, 'Order successful')
                    return redirect('/payment/')
        except Member.DoesNotExist:
            messages.error(request, 'Record Not Found')
            return redirect(f'/dashboard/{userID}/subscribe/')
            

def payment(request):
    if request.method=='GET':
        try:
            userID = request.session['userid']
            ref = request.session['refno']
            subord = Sub.objects.get(sub_refno=ref)
            context = {'userID':userID, 'subord':subord}
            return render(request, 'payment.html', context)
        except Member.DoesNotExist:
            messages.error(request, 'Payment unsuccessful')
            return redirect('/suborder')


def subpayment(request):
    if request.method=='POST':
        try:
            userID = request.session['userid']
            ref = request.session['refno']
            amt = request.POST.get('amt')
            subid = request.POST.get('subid')
            if amt !="" or subid !="":
                usdid = Member.objects.get(id=userID)
                suid = Sub.objects.get(id=subid)
                pyt=Payment.objects.create(pay_amount=amt,
                                           pay_date=datetime.datetime.now(),
                                           pay_status='pending',
                                           pay_memberId = usdid,
                                           pay_refno = ref,
                                           pay_subId = suid)
                pyt.save()
                ordpay = Payment.objects.get(pay_refno=ref)
                
                data = {"email":usdid.email, "amount":int(ordpay.pay_amount)*100, "reference":ordpay.pay_refno}
                print(data)
                headers = {"Content-Type":"application/json", "Authorization":"Bearer sk_test_9ebd9bc239bcde7a0f43e2eab48b18ef1910356f"}
                response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))
                
                rspjson = json.loads(response.text)
                print(rspjson)
                
                if rspjson.get('status')==True:
                    print(rspjson['data']['authorization_url'])
                    authur1 = rspjson['data']['authorization_url']
                    return redirect(authur1)
                else:
                    return "Please try again"
            else:
                messages.error(request, 'Payment unsuccessful')
                return redirect('/payment/')
        except Member.DoesNotExist:
            messages.error(request, 'something just happened')
            return redirect('/payment/')


def payverify(request):
    if request.method=='POST':
        try:
            userID = request.session['userid']
            ref = request.session['refno']
            reference = request.args.get('reference')
            headers = {"Content-Type":"application/json", "Authorization":"Bearer sk_test_9ebd9bc239bcde7a0f43e2eab48b18ef1910356f"}
            response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
            rsp = response.json()
            if rsp['data']['status']=='success':
                amt = rsp['data']['status']
                ipaddress = rsp['data']['ip_address']
                p = Payment.objects.get(pay_refno=ref)
                p.pay_status = 'paid'
                p.save()
                s = Sub.objects.get(sub_refno = ref)
                s.sub_status = 'active'
                s.save()
                messages.success(request, 'Your subscription is now Active')
                return redirect(f'/dashboard/{userID}/')
            else:
                p = Payment.objects.get(pay_refno=ref)
                p.pay_status = 'failed'
                p.save()
                messages.success(request, 'Your subscription is still pending')
                return redirect(f'/dashboard/{userID}/')
        except Member.DoesNotExist:
            
            return redirect(f'/dashboard/{userID}/')


def logout(request, id):
    userID = request.session['userid']
    if userID is not None:
        request.session.pop('userid', None)
        return redirect('/')
    else:
        return redirect('/')
    
def testing(request):
    mydata = Member.objects.all().order_by('lastname', '-id').values()
    # select * from members where lastname = 'Mikel' or id = 2;
    template = loader.get_template('try.html')
    context = { "my":mydata}
    return HttpResponse(template.render(context, request))


# def custom_404(request, exception):
#     template = loader.get_template('404.html')
#     return HttpResponse(template.render())

# def custom_500(request):
    # template = loader.get_template('404.html')
    # return HttpResponse(template.render())
    # return redirect('/')
    
