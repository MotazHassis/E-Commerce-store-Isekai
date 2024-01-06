from django.contrib import admin
from .models import *
from django.utils.html import format_html
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username',
                    'email',
                    'avatar_pic',
                    ]
    def avatar_pic(self,obj):
        return format_html('<img src="{0}" width="auto" height="50px">'.format(obj.avatar.url))

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'price',
                    'discount_price',
                    'category',
                    'image',
                    )
    def image(self,obj):
        return format_html('<img src="{0}" width="auto" height="50px">'.format(obj.item_image.url))
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [#'user',
                    'get_user',
                    'ordered',
                    'item',
                    'quantity',
                    ]
    def get_user(self,obj):#motaz
        return [user.username for user in obj.user.all()]#motaz
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code',
                    'amount',
                    ]  
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ref_code',
                    'get_order_items',#motaz
                    'ordered',
                    'shipping_address',
                    'payment',
                    'start_date',
                    'ordered_date',
                    ]
    def get_order_items(self,obj):#motaz
        return [items for items in obj.items.all()]#motaz  

class AddressAdmin(admin.ModelAdmin):
    list_display = ['uploaded_by',
                    'country',
                    'full_name',
                    'mobile_number',
                    'Apartment',
                    'street',
                    'landmark',
                    'town',
                    ]
    
class payment_infoAdmin(admin.ModelAdmin):
    list_display = ['card_holder_name',
                    'card_number',
                    'expiry_date',
                    'cvc',
                    'order',
                    ]
    
admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address,  AddressAdmin)
admin.site.register(payment_info,  payment_infoAdmin)




