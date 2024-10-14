from django import forms
from django.core.exceptions import ValidationError
from CustomUserApp.models import CustomUser

class RegisterForm(forms.ModelForm):
    first_name=forms.CharField(label='First Name',required=True)
    last_name=forms.CharField(label='Last Name', required=True)
    email=forms.EmailField(label='Email',required=True)
    city=forms.CharField(label='City',required=True)
    state=forms.CharField(label='State',required=True)
    country=forms.CharField(label='Country',required=True)
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
                                                                                             
    class Meta:        
        model=CustomUser
        fields=('first_name','last_name','email','city','state','country','password1','password2')
        
        
    def clean_email(self):
        email=self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email is already in use')
        return email
                                                                                                                        
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 !=password2 :
            raise ValidationError("Two passowrds didn't match ")
        if len(password1)<8:
            raise ValidationError('Password length should be of minimum 8 characters')
        
        if not any(x.isupper() for x in password1):
            raise ValidationError("Password Should contain one Upper Case letter")
          
        if not('@' or '#' or '$')  in password1:
            raise ValidationError("Password should contain atleast One Special Character . Only @ or $ or # are allowed ")
        return password2 

        
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=CustomUser
        fields={'email','password'}


class forgot_password_Form(forms.Form):
    email=forms.EmailField(label='Enter Email',required=True)
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Enter the email you used during your account creation  ')
        return email        
        
    class Meta:
        model=CustomUser
        fields={'email'}
        
        
class forgot_password_done_Form(forms.Form):

    password1=forms.CharField(label='Type New Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Retype New Password',widget=forms.PasswordInput)
    
    class Meta:
        model=CustomUser
        fields={'password1','password2'}
        
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2 :
            raise ValidationError("Two passowrds didn't match ")
        if len(password2)<8:
            raise ValidationError('Password length should be of minimum 8 characters')
        
        if not any(x.isupper() for x in password2):
            raise ValidationError("Password Should contain one Upper Case letter")
        
        if not('@' or '#' or '$')  in password2:
            raise ValidationError("Password should contain atleast One Special Character . Only @ or $ or # are allowed ")
        return password2 


class Change_Password_Form(forms.Form):
    password1=forms.CharField(label="Enter Your Old Password",widget=forms.PasswordInput,required=True)
    password2=forms.CharField(label="Enter New Password ",widget=forms.PasswordInput)
    password3=forms.CharField(label="Re-Enter New Password",widget=forms.PasswordInput)

    class Meta:
        model=CustomUser
        fields={'password1','password2','password3'}
     
    def clean_password3(self):
        print("inside form method")
        password2=self.cleaned_data.get('password2')
        password3=self.cleaned_data.get('password3')
        
        print("password2",password2)
        print("password3",password3)
        
        if password2 and password3 and password2 !=password3 :
            raise ValidationError("Two passowrds didn't match ")
        if len(password2)<8:
            raise ValidationError('Password length should be of minimum 8 characters')
        if not any(x.isupper() for x in password2):
            raise ValidationError("Password Should contain one Upper Case letter")
        if not('@' or '#' or '$')  in password2:
            raise ValidationError("Password should contain atleast One Special Character . Only @ or $ or # are allowed ")

        return password3


class Update_User_Form(forms.ModelForm):
    pass

    class Meta:
        model=CustomUser
        fields=('email','first_name','last_name','city','state','country')
    

class UpdateProfileForm(forms.ModelForm):
    pass

    class Meta:
        model=CustomUser
        fields=('email','first_name','last_name','city','state','country')
    
