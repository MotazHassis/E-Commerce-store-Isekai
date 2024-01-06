from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
from django.utils import timezone
import random
import string
from django.conf import settings
import stripe
from .models import OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash




# Create your views here.
def index(request):
    specific_user = None
    if 'user_id' in request.session:
        specific_user = User.objects.get(id=request.session['user_id'])

    context = {
        'allitems': Item.objects.all(),
        'allorderitem': OrderItem.objects.all(),#why we add this here, we don't use it//Motaz
        'specific_user': specific_user,
    }
    return render(request, 'home.html', context)
def product(request,id):
    if 'user_id' in request.session:
        this_item=Item.objects.get(id=int(id))
        saving=this_item.price-this_item.discount_price
        context={
            'this_item':this_item,
            'saving': saving,
            'specific_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request,'product_main_page.html',context)
    else:
        return redirect ('/login')

def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator1(request.POST)
        if len(errors) > 0 :
            return redirect('/register')
        else:
            hash1= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            registered_user = User.objects.create(
                username=request.POST['username'],
                email=request.POST['email'],
                password=hash1,
                )
            messages.success(request, "Registered successfully")
            request.session['user_id']=registered_user.id
            request.session['username']=registered_user.username

            return redirect('/')

    else:
        return render(request,'register.html')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['lemail'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['lpassword'].encode(), logged_user.password.encode()):
                    request.session['user_id']=logged_user.id
                    request.session['username']=logged_user.username

                    return redirect('/')
            else:
                err={}
                err['authentication']= 'Invalid authentication'
                request.session['authentication']=err['authentication']
                print(request.session['authentication'])
                return redirect ('/login')

        else:
            err={}
            err['authentication']= 'Invalid authentication'
            request.session['authentication']=err['authentication']
            print(request.session['authentication'])
            return redirect ('/login')
    else:
        return render(request,'login.html')
def add_to_cart(request,id):
    if 'user_id' in request.session:
        this_user=User.objects.get(id=request.session['user_id'])
        this_item=Item.objects.get(id=int(id))
        amount=request.POST['quantity']
        order_item=OrderItem.objects.create(
            # user=this_user,
            item=this_item,
            quantity=amount
        )
        order_item.user.add(this_user)#motaz
        return redirect('/cart')
    else:
        return redirect('/login')
def cart(request):
    if 'user_id' in request.session:
        this_user=User.objects.get(id=request.session['user_id'])
        total=0
        saving = 0
        for item in this_user.order_items_for_user.all():
            print(item.item.price)
            print(item.quantity)
            total+=(item.item.price*item.quantity)
            saving += (item.item.price - item.item.discount_price) * item.quantity
            request.session['saving'] = saving
            request.session['total'] = total
        context={
            'allitems_in_order':this_user.order_items_for_user.all(),
            'total':total,
            'specific_user': User.objects.get(id=request.session['user_id'])

        }
        return render(request, 'shopping_cart.html',context)

    else:
        return redirect('/login')

def delete_order_item(request,id):
    this_order_item=OrderItem.objects.get(id=int(id))
    this_order_item.delete()

    return redirect('/cart')
def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
    return redirect('/')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////

def search_results(request):
    search = Item.objects.filter(title__contains=request.POST['search_ajax'])
    if search:            
            context={
                'search':search.all()
            }
            
    return render(request,'ajax_search.html',context)


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def your_account(request):
    if not 'user_id' in request.session:
        return redirect('/login')
    else:    
        context = {
        'specific_user': User.objects.get(id=request.session['user_id'])
    }
        return render(request, 'your_account.html', context)

def your_addresses(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        context={
            'alladdresses': Address.objects.all(),
            'specific_user': User.objects.get(id=request.session['user_id'])

        }
        return render (request, "your_addresses.html", context)


def add_new_address(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:

        if request.method == 'GET':
            context = {
                'specific_user': User.objects.get(id=request.session['user_id'])
            }
            return render(request, 'add_new_address.html',context)
        if request.method == 'POST':
            errors = Address.objects.basic_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/your_addresses')
            else:
                address=Address.objects.create(uploaded_by=User.objects.get(id=request.session['user_id']), country=request.POST['country'],full_name=request.POST['full_name'], mobile_number=request.POST['mobile_number'],PIN_code=request.POST['PIN_code'], Apartment=request.POST['Apartment'],street=request.POST['street'],landmark=request.POST['landmark'], town=request.POST['town'])
            return redirect('/your_addresses')

def select_address(request):
        if not 'user_id' in request.session:
            messages.error(request,"You have to login first")
            return redirect('/login')
        else:
            if request.method == 'GET':
                context = {
                'alladdresses': Address.objects.all(),
                'specific_user': User.objects.get(id=request.session['user_id'])
                }
                return render(request, 'select_address_motaz.html' ,context)


def select_payment_method(request,id):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        this_address=Address.objects.get(id=int(id))#motaz
        request.session['user_address_id']=this_address.id
        if request.method == 'GET':
            context={
            'specific_user': User.objects.get(id=request.session['user_id'])

        }
            return render (request, "select_payment_method.html", context)
        if request.method == 'POST':
            if 'paymentMethod' in request.POST:
                request.session['paymentMethod'] = request.POST['paymentMethod']
                return redirect('/review_order')


def review_order(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        this_address=Address.objects.get(id=request.session['user_address_id'])
        context = {
            # 'alladdresses': Address.objects.all(),
            'specific_user': User.objects.get(id=request.session['user_id']),
            'this_address':this_address#motaz
        }
        return render(request, "review_order.html", context)

def create_order(request):
    if 'user_id' in request.session:
        specific_user=User.objects.get(id=request.session['user_id'])
        def create_ref_code():
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        ref=create_ref_code()
        this_address=Address.objects.get(id=request.session['user_address_id'])
        specific_order = Order.objects.create(user=specific_user,
                                            ref_code=ref,
                                            payment=request.session.get('paymentMethod'),
                                            ordered=True,
                                            shipping_address=this_address,
                                            total_payed_amount=float(request.session['total'])
                                            )#motaz
        request.session['order_id']=specific_order.id#motaz
        all_item_order=specific_user.order_items_for_user.all()
        for item in all_item_order:
            specific_order.items.add(item)
    return redirect('/complete_payment')

def complete_payment(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        if request.method == 'POST':
            errors = payment_info.objects.basic_validator_payment(request.POST)
            if len(errors) > 0 :
                print('not')
                return redirect('/complete_payment')
            else:
                specific_user= User.objects.get(id=request.session['user_id'])
                specific_order=Order.objects.get(id=request.session['order_id'])
                payment_info.objects.create(
                    order=specific_order,
                    card_number=request.POST['cardNumber'],
                    expiry_date=request.POST['expiryDate'],
                    cvc=request.POST['cvc'],
                    card_holder_name=request.POST['cardHolderName']
                    )
                print('done')
                return redirect('/complete')
        else:
            specific_user= User.objects.get(id=request.session['user_id'])#motaz
            all_user_items=specific_user.order_items_for_user.all()#motaz
            
            print('notdone')
            context = {
            'all_user_items':all_user_items,
            'specific_user': specific_user
            }
            return render(request, "complete_payment.html", context)

#///////////////////////////////////////////////////////////////////motaz
def complete(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        specific_user= User.objects.get(id=request.session['user_id'])
        all_user_items=specific_user.order_items_for_user.all()
        for item in all_user_items:
            item.user.remove(specific_user)
        
        return redirect('/invoice')
    

def cancel_order_items(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        specific_user= User.objects.get(id=request.session['user_id'])
        all_user_items=specific_user.order_items_for_user.all()
        for item in all_user_items:
            item.delete()
        return redirect('/')

def cancel_order(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        specific_user= User.objects.get(id=request.session['user_id'])
        all_user_items=specific_user.order_items_for_user.all()
        for item in all_user_items:
            item.delete()
        specific_order=Order.objects.get(id=request.session['order_id'])
        specific_order.delete()
        return redirect('/')

def user_orders(request):
    if not 'user_id' in request.session:
        messages.error(request,"You have to login first")
        return redirect('/login')
    else:
        specific_user= User.objects.get(id=request.session['user_id'])
        all_orders=Order.objects.filter(user=specific_user).order_by("-id")
        context = {
            'specific_user': specific_user,
            'all_orders':all_orders,
            
        }
        return render(request, "your_orders.html", context)
# /////////////////////motaz 
def change_password(request):
    if request.method == 'POST':
        errors= User.objects.basic_validator2(request.POST)
        if len(errors) > 0 :
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/change-password')
        else:
            this_user_email=User.objects.filter(email=request.POST['email'])
            if this_user_email:
                this_user=this_user_email[0]
                if bcrypt.checkpw(request.POST['currentPassword'].encode(), this_user.password.encode()):
                    hash1= bcrypt.hashpw(request.POST['newpassword'].encode(), bcrypt.gensalt()).decode()
                    if request.POST['newpassword']==request.POST['password_confirm']:
                        this_user.password=hash1
                        this_user.save()
                        messages.success(request, "Password Changed successfully")
                        return redirect('/')
                    else:
                        messages.error(request, "new password don't match confirm password")
                        return render(request, 'change_password.html')
                else:
                        messages.error(request, "Wrong Password")
                        return render(request, 'change_password.html')    
            else:
                messages.error(request, "Invalid authentifications")
                return render(request, 'change_password.html')

    else:
        
        return render(request, 'change_password.html')
    
    
def search_order(request):
    
    search = Order.objects.filter(ref_code__startswith=request.POST['search_order_ajax'])
    if search:
            context={
                'search':search.all()
            }
            
    return render(request,'ajax_search_order.html',context)

def invoice(request):
    context={
                'specific_order': Order.objects.get(id=request.session['order_id'])
            }
    return render(request,'index.html', context)
def delete_address(request, id):
    this_address=Address.objects.get(id=int(id))
    this_address.delete()
    return redirect('/your_addresses')