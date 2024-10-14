from django.contrib import admin
from CustomUserApp.models import *
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display=['name','description','Cat_name','price']


class AdminCategory(admin.ModelAdmin):
    list_display=['name']

class AdminOrder(admin.ModelAdmin):
    model=Order
    list_display=['id','Order_Id','user','item_name','price','quantity','order_date','total_price','payment_id','invoice_number']

    # def Name(self,obj):
    #     return f"{obj.user.first_name} {obj.user.last_name}"


admin.site.register(CustomUser)
admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Order,AdminOrder)
