from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from CustomUserApp.managers import CustomUserManager

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    country=models.CharField(max_length=30)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    forget_password_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
 
    
class Category(models.Model):
    Cat_name=models.CharField(max_length=50 )

    def __str__(self):
        return self.Cat_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=300)
    Cat_name=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='ProductImages/')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f" {self.quantity} of {self.product.name}"


class Order(models.Model):
    Order_Id=models.IntegerField(null=True,blank=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=50,blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    quantity=models.IntegerField(blank=True,null=True)
    order_date=models.DateTimeField(auto_now_add=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    is_paid=models.BooleanField(default=False)
    payment_id=models.CharField(max_length=100)
    invoice_number=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return f"Order {self.id} by {self.user.first_name}"
    

    
# class Cart(models.Model):
#     user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f" Cart of {self.user.first_name} {self.user.last_name}"