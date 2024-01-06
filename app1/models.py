from django.db import models
import bcrypt
import re
# from django import forms

class UserManager(models.Manager):
    def basic_validator1(self, postData):
        errors={}
        if len(postData['username']) < 2 :
            errors['username']= 'Username should be more than 2 characters'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']= 'Invalid Email Address'
        if len(postData['password']) < 8:
            errors['password']= 'Please Password must be at least 8 characters.'
        if postData['password'] != postData['confirm']:
            errors['confirm']= 'Password not match'
        return errors
    def basic_validator2(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']= 'Invalid Email Address'
        if len(postData['newpassword']) < 8:
            errors['newpassword']= 'Please Password must be at least 8 characters.'
        if postData['newpassword'] != postData['password_confirm']:
            errors['password_confirm']= 'Password not match'
        return errors
class payment_infoManager(models.Manager):

    def basic_validator_payment(self, postData):
        errors={}
        if len(postData['cardNumber']) < 16 :
            errors['cardNumber']= 'cardNumber should be more than 15 digit'
        
        if len(postData['expiryDate']) < 5 :
            errors['expiryDate']= 'Invalid expiry Date'
        if len(postData['cvc']) < 3:
            errors['cvc']= 'cvc must be 3 digit.'
        if len(postData['cardHolderName']) < 2 :
            errors['cardHolderName']= 'card Holder Name should be more than 2 characters'
        return errors


class User(models.Model):
    username=models.CharField(max_length=64)
    email=models.CharField(max_length=255)
    password=models.TextField()
    avatar=models.ImageField(upload_to='image',default='image/default.jpg',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects= UserManager()
    def __str__(self):
        return self.username

class Item(models.Model):
    title=models.CharField(max_length=100)
    item_image=models.ImageField(upload_to='image',default='image/default.jpg',blank=True)
    desc=models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ManyToManyField(User,related_name='order_items_for_user',blank=True)#motaz
    # user = models.ForeignKey(User,related_name='order_items_for_user',on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        # return self.user.username + self.item.title
        return self.item.title +'   ||' +'quantity:'+str(self.quantity)#motaz

class Coupon(models.Model):#we have to delete this later\\motaz
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    def __str__(self):
        return self.code


class AddressManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['country']) < 5 :
            errors['country']= 'country should be more than 5 characters'
        if len(postData['full_name']) < 3 :
            errors['full_name']= 'full_name should be more than 3 characters'
        if len(postData['PIN_code']) < 5 :
            errors['PIN_code']= 'Username should be more than 5 characters'
        if User.objects.filter(email=postData['PIN_code']).exists():
            errors["PIN_code"] = "This PIN_code is already exists"

        return errors

class Address(models.Model):
    uploaded_by = models.ForeignKey(User, related_name ='address', on_delete = models.CASCADE)
    country=models.CharField(max_length=225)
    full_name=models.CharField(max_length=225)
    mobile_number=models.CharField(max_length=225)
    PIN_code=models.CharField(max_length=225)
    Apartment=models.CharField(max_length=225)
    street=models.CharField(max_length=225)
    landmark=models.CharField(max_length=225)
    town=models.CharField(max_length=225)
    objects= AddressManager()
    def __str__(self):
        return str(self.uploaded_by.username)



class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem,related_name='items_in_order')
    ordered = models.BooleanField(default=False)
    total_payed_amount=models.FloatField()#i add this \\motaz
    # shipping_address = models.CharField(max_length=255,blank=True, null=True)
    shipping_address = models.ForeignKey(Address,on_delete=models.CASCADE)#i add this \\motaz
    payment = models.CharField(max_length=255,blank=True, null=True)
    being_delivered = models.BooleanField(default=False)#we have to delete this later\\motaz
    received = models.BooleanField(default=False)#we have to delete this later\\motaz
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)#we have to delete this later\\motaz
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class payment_info(models.Model):#i add this \\motaz
    order=models.ForeignKey(Order,related_name='order_payment_info',on_delete=models.CASCADE )
    card_number=models.CharField(max_length=255)
    expiry_date=models.CharField(max_length=5)
    cvc=models.CharField(max_length=3)
    card_holder_name=models.CharField(max_length=255)
    objects= payment_infoManager()
    def __str__(self):
        user=self.order.user
        return 'Ordered by : '+str(user)+' || Order ID : '+str(self.order.id)













