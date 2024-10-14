from django import utils
from django.shortcuts import render,redirect
from django.http import HttpResponse
from CustomUserApp.forms import *
from django.contrib.auth import authenticate,login,logout
from CustomUserApp.models import CustomUser,Product,Category,CartItem,Order
from django.contrib import messages
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from CustomUserApp.forms import forgot_password_Form,forgot_password_done_Form,Change_Password_Form
from CustomUserApp.helpers import *
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from CustomUserApp.models import Product
from random import randint
from django.urls import reverse
# import paypalrestsdk
import stripe 


import reportlab
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse




# -----------Registration-----------------------------
def Signup(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            password=form.cleaned_data['password1']
            new_user.set_password(password)
            new_user.is_active=False
            new_user.save()
            # -----------Email Verification-------------
            email=form.cleaned_data.get('email')
            obj=CustomUser.objects.get(email=email)
            
            token=default_token_generator.make_token(obj)
            uid=urlsafe_base64_encode(force_bytes(new_user.pk))
            
            subject='Email Verification Link'
            message=f'Hi, Click on the link to verify your mail http://127.0.0.1:8000/activate/{uid}/{token}/ '
            email_from = settings.EMAIL_HOST_USER
            recipient_list=[email]
            mail(subject,message,email_from,recipient_list)
            return redirect('Signin')
    else:
        form=RegisterForm()
    return render(request,'CustomUserApp_Register.html',{'form':form})

# ----  For Activating the link --------------------
def activate(request, uidb64, token):  
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)
    if not user.is_active:
        if user is not None and default_token_generator.check_token(user, token):  
            user.is_active = True  
            user.email_verified=True
            user.save() 
    else:
        return HttpResponse("link is invalid")      
    return render(request,'CustomUserApp_Activate.html')


# ---------  LogIn ----------
def Signin(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password1=form.cleaned_data.get('password')
            userr=CustomUser.objects.get(email=email)
            
            res=check_password(password1,userr.password)
            
            print("res",res)
            print("email",email)
            print("psword",password1)
            
            print(userr.is_active)
            if not userr.is_active:
                return HttpResponse("Please Verify your mail to activate your account")
            user=authenticate(email=email,password=password1)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('Home')
            else:
                return HttpResponse("Invalid Details Provided")
    else:
        form=LoginForm()
    return render(request,'CustomUserApp_Login.html',{'form':form})


#------------Home---------------------
def Home(request):
    products=None
    Categories=Category.objects.all()
    categoryID= request.GET.get('category')
    if categoryID:
        products=Product.objects.filter(Cat_name_id=categoryID)
    else:
        products=Product.objects.all()
        print("products",products)
    return render(request,'CustomUserApp_Homepage.html',{'products_data':products,'Categories':Categories})

# --------------------Dashboard----------------------
@login_required(login_url='Signin')
def dashboard(request):
    user=None
    if request.user.is_superuser:
        user=CustomUser.objects.all()
    
    orders=Order.objects.filter(user=request.user)
    return render (request,'CustomUserApp_Dashboard.html',{'userdata':user,'orders':orders})

#  ---------forgot Password Request-----
@login_required(login_url='Signin')
def forgot_password(request):
    if request.method=='POST':
        form=forgot_password_Form(request.POST)
        
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user_obj=CustomUser.objects.get(email=email)
            print(user_obj)
            token=default_token_generator.make_token(user_obj)
            uid=urlsafe_base64_encode(force_bytes(user_obj.pk))
            print("token",token)
            print("uid",uid)
            
            subject='Your reset password link'
            message= f'Hi , Click on the link to reset your passowrd http://127.0.0.1:8000/forgot_password_done/{uid}/{token}/'
            email_from= settings.EMAIL_HOST_USER
            recipient_list=[email]
            mail(subject,message,email_from,recipient_list)
            return HttpResponse("Email sent")
    else:
        form =forgot_password_Form()
    return render(request,'reset_password.html',{'form':form})
                                        
# ---------- Forgot Passowrd Done-----------
def forgot_password_done(request,uidb64,token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user= CustomUser.objects.get(pk=uid)
    print("user",user)
    print("uid",uid)
    print("token",token)
    if request.method=='POST':
        form=forgot_password_done_Form(request.POST)
        if form.is_valid():
            if user is not None and default_token_generator.check_token(user, token):
                email=CustomUser.objects.get(email=user)
                password= form.cleaned_data.get('password2')
                obj=CustomUser.objects.get(email= email)
                obj.set_password(password)
                obj.save()
                return HttpResponse("Password Changed Successfully")
    else:
        form=forgot_password_done_Form()
    return render (request,'forgot_password_done.html',{'form':form})

# -------------LogOut---------------
@login_required(login_url='Signin')
def signout(request):
    logout(request)
    return redirect('Home')

# -------------Change Password---------------------
@login_required(login_url='Signin')
def change_password(request):
    if request.method=='POST':
        form=Change_Password_Form(request.POST)  
        if form.is_valid():
            entered_old_pasword=form.cleaned_data.get("password1")
            password=form.cleaned_data.get("password3")
            user=request.user
            passwordd=user.password
            obj=CustomUser.objects.get(email=user)
            res=check_password(entered_old_pasword,passwordd)
            print(res)
            if res == True:
                obj.set_password(password)
                obj.save()
                messages.success(request,"You have successfully changed your password")
            else:
                messages.error(request,"Your entered old password is incorrect")
    else:
        form=Change_Password_Form()
    return render (request,'CustomUserApp_Change_Password_Request.html',{'form':form})

# ---------------------------------Delete User Data----------------------------------------------
@login_required(login_url='Signin')  
def DeleteUserData(request,id):
    data=CustomUser.objects.get(id=id)
    data.delete()
    return redirect('dashboard')

# ----------------------------------Update User Data-----------------------------------------------
@login_required(login_url='Signin')
def UpdateUserData(request,id):
    obj=CustomUser.objects.get(id=id)
    form=Update_User_Form(instance=obj)
    if request.method=='POST':
        obj=CustomUser.objects.get(id=id)
        if form.is_valid():
            res=Update_User_Form(instance=obj,data=request.POST)
            res.save()
            return redirect('dashboard')
    return render (request,'CustomUserApp_UpdateUserdata.html',{'form':form})

# ----------------Update Profile-------------------
@login_required(login_url="Signin")
def UpdateProfile(request):
    user=request.user
    print("user",user)
    obj=CustomUser.objects.get(email=user)
    form=UpdateProfileForm(instance=obj)
    if request.method=='POST':
        obj=CustomUser.objects.get(id=user.id)
        res=UpdateProfileForm(instance=obj,data=request.POST)
        res.save()
        return redirect('dashboard')
    return render (request,'CustomUserApp_Update_Profile.html',{'form':form})

# ------------------ AboutUs Page----------------------
def AboutUs(request):
    return render (request,'CustomUserApp_AboutUs.html')

# ------------------Add To Cart---------------------
@login_required(login_url='Signin')
def AddToCart(request,id):
    product=Product.objects.get(id=id)
    print('id',id)
    cart_item,created=CartItem.objects.get_or_create(user=request.user,product=product)
    print("created",created)
    if not created :
        cart_item.quantity+=1
        cart_item.save()
    messages.success(request,'Added to Cart')
    return redirect('Home')

# -----------------CheckOut----------------------------------
@login_required(login_url='Signin')
def CheckOut(request):
    cart_items=CartItem.objects.filter(user=request.user)

    amount=0
    for i in cart_items:
        quantiy=i.quantity
        amount += (i.product.price )*quantiy
        
    return render(request,"CustomUserApp_CheckOut_page.html",{'cart_items':cart_items,'amount':amount})


# ---------------------------Remove Item From Cart----------------
@login_required(login_url='Signin')
def RemoveItem(request,id):
    print("id",id)
    CartItem.objects.get(id=id).delete()
    return redirect("CheckOut")


# ------------------------Buy Single Product-----------------
@login_required(login_url='Signin')
def BuyNow(request,id):
    if request.method=="POST":
        quantity=request.POST.get('Quantity')
        
        print('quantity',quantity)
        CartItem.objects.filter(id=id).update(quantity=quantity)
        
    item=CartItem.objects.filter(id=id)
    print('item',item)
    return render(request,'CustomUserApp_BuyNow_page.html',{'item':item})

# -----------------------Buy All---------------------------------
@login_required(login_url='Signin')
def BuyAll(request):
    items=CartItem.objects.filter(user=request.user)
    amount=0
    for i in items:
        quantiy=i.quantity
        amount += (i.product.price )*quantiy
    return render(request,'CustomUserApp_BuyNow_page.html',{'items':items,'amount':amount})


# Stripe Payment 
stripe.apikey = settings.STRIPE_SECRET_KEY

#------------------------------Make Payment----------------------------------------
def create_checkout_session_for_all(request):
    cart_items=CartItem.objects.filter(user=request.user)
    line_items=[]
    for item in cart_items:
        line_items.append({
            'price_data':{
                'currency':'inr',
                'product_data':{
                    'name':item.product.name
                },
                'unit_amount':int (item.product.price*100),
            },
            'quantity':item.quantity,
        })
        
    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('CheckOut')),
    )
    return redirect(session.url,code=303)


@login_required(login_url='Signin')
def create_checkout_session_for_one(request,id):
    request.session['item_id']=id
    
    cart_item=CartItem.objects.filter(id=id)
    print("cartitem",cart_item)
    
    line_items=[]
    for item in cart_item:
        line_items.append({
            'price_data':{
                'currency':'inr',
                'product_data':{
                    'name':item.product.name
                },
                'unit_amount':int (item.product.price*100),
            },
            'quantity':item.quantity, 
        }) 
        
        
    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        metadata= { 
            "name": str(item.product.name),
            "price": str(item.product.price),
            "quantity":str(item.quantity),
        },
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success'))+'?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('CheckOut')),
    )
    
    return redirect(session.url,code=303)


def success(request):
    id=request.session['item_id']
    print('item_id',id)
    session_id=request.GET.get('session_id')
    session= stripe.checkout.Session.retrieve(session_id)
    payment_id=session.payment_intent
    item_name=session.metadata.name
    price=session.metadata.price
    Quantity=session.metadata.quantity
    
    print('payment id',payment_id)
    print('session_id',session_id)
    # print('session',session)
    
    item=CartItem.objects.filter(id=id)
    print(item)
    amount=0
    for i in item:
        quantity=i.quantity
        amount+= (i.product.price)*quantity
        orderId=randint(100000,999999)
        invoice_number=randint(1000000000,9999999999)
        order= Order.objects.create(user=request.user,total_price=amount,is_paid=True,payment_id=payment_id,item_name=item_name,price=price,quantity=Quantity,Order_Id=orderId,invoice_number=invoice_number)
        order.save()
        i.delete()

    orderdata=Order.objects.filter(payment_id=payment_id)
    print('orderdata',orderdata)
    for x in orderdata:
        print("orderid",x.id)
    # sending email after successfull payment
    email=request.user
    subject='EZ Cart Orders'
    message= "Your order is placed succesfully "
    email_from= settings.EMAIL_HOST_USER
    recipient_list=[email]
    mail(subject,message,email_from,recipient_list)
    return render(request, 'CustomUserApp_payment_success.html',{'orderdata':orderdata})


def cancel(request):
    return render(request, 'CustomUserApp_payment_failed.html')


def get_invoice(request,id):
    data=Order.objects.filter(id=id)
    for x in data:
        order_id = str(x.Order_Id)
        payment_id = str(x.payment_id)
        name = x.user.first_name
        item = x.item_name
        price = str(x.price)
        quantity = str(x.quantity)
        order_date = str(x.order_date)
        total_price = str(x.total_price)
        invoice_number = str(x.invoice_number)
      
    result=generate_pdf(order_id,payment_id,name,item,price,quantity,order_date,total_price,invoice_number)
    response = HttpResponse(content_type='application/pdf')
    response.write(result.dest.getvalue())
    return response
        
    


# def get_invoice(request,id):
#     data=Order.objects.filter(id=id)
#     print("data",data)
    
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 100, "Hello world.")
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename="EZCartInvoice.pdf")
