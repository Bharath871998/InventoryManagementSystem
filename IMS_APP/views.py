from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import auth, User   
from django.contrib import messages       
from django.db.models import Sum
from .models import Product, StockLog
from .forms import ProductForm
# Create your views here.

# Product Stock Updation Only by Admin(Staff) user
# Stock Changes made by Admin
'''
Function operation: When the Admin changes it's quantity by adding or removing the quantity with reason,
then this will reflects in Products table quantity and stock level status and also alerts when stock is less than or equal too 5 units
'''
@user_passes_test(lambda user: user.is_staff)
def change_product_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        quantity_change = int(request.POST.get('quantity_change'))
        reason = request.POST.get('reason')

        # Update the product's stock and create a StockLog entry
        if reason == StockLog.ADDITION:
            product.quantity += quantity_change
        elif reason == StockLog.REMOVAL:
            product.quantity -= quantity_change
        
        # Ensure the quantity does not go below zero
        product.quantity = max(product.quantity, 0)
        product.save()

        # Creating a StockLog entry
        StockLog.objects.create(
            product=product,
            quantity_changed=quantity_change,
            reason=reason,
            date_changed=timezone.now()
        )

        return redirect('product_detail', pk=product.pk)

    return render(request, 'change_stock.html', {'product': product})


# CRUD Operations for only Admin(Staff Member)
# CREATE Operation
@user_passes_test(lambda user: user.is_staff)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products') # Redirecting to Product List after Product creation
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})


# UPDATE Opertaion
@user_passes_test(lambda user: user.is_staff)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


# DELETE Operation
@user_passes_test(lambda user: user.is_staff)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'delete_product.html', {'product': product})

# End Of CRUD Operations For Admin(Staff) user

# Product List View only for regular Users
# All Product List
def products(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# Single Product Details 
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


# Admin Dashboard Report
# views.py (updated report_view)
def report_view(request):
    products = Product.objects.all()
    
    # Filtering
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category=category_filter)

    supplier_filter = request.GET.get('supplier')
    if supplier_filter:
        products = products.filter(supplier=supplier_filter)

    stock_level_filter = request.GET.get('stock_level')
    if stock_level_filter:
        products = products.filter(quantity__lte=stock_level_filter)

    total_inventory_value = products.aggregate(Sum('quantity', field='quantity * price'))['quantity__sum'] or 0

    return render(request, 'report.html', {
        'total_inventory_value': total_inventory_value,
        'products': products,
    })


# User Registration and Authentication and Logging out for regular Users
# Signup
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching..')    
            return redirect('signup')
    else:
        return render(request,'signup.html')
    

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request, "login.html")
    

def logout(request):
    auth.logout(request)    
    return redirect("/")


