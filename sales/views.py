from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Order, OrderItem

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum, F, Count, DecimalField
from django.shortcuts import render


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # 创建用户
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, '注册成功，请登录')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'sales/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, '用户名或密码错误')
    else:
        form = UserLoginForm()
    return render(request, 'sales/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')



@login_required
def index(request):
    """
    Home: redirect admins to dashboard, customers to product list.
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('product_list')

def product_list(request):
    """
    Publicly viewable product list (customers will only get here if logged in).
    """
    query = request.GET.get('q', '')
    qs = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'sales/product_list.html', {
        'products': qs,
        'query': query
    })


@login_required
@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.stock <= 0:
        messages.error(request, "Sorry, this item is out of stock.")
        return redirect('product_list')

    order = Order.objects.create(user=request.user)  # create order
    OrderItem.objects.create(order=order, product=product, quantity=1)
    product.stock -= 1
    product.save()

    # Directly render confirmation page—no extra URL needed
    return render(request, 'sales/order_success.html', {'product': product})


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Basic aggregates
    total_users  = User.objects.count()
    total_orders = Order.objects.count()
    total_items  = OrderItem.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    total_revenue = OrderItem.objects.aggregate(
        revenue=Sum(
            F('quantity') * F('product__price'),
            output_field=DecimalField()
        )
    )['revenue'] or 0

    # Orders per user: list of [username, order_count]
    orders_per_user_qs = (
        Order.objects
             .values('user__username')
             .annotate(count=Count('id'))
             .order_by('-count')
    )

    labels = [entry['user__username'] for entry in orders_per_user_qs]
    data   = [entry['count'] for entry in orders_per_user_qs]

    context = {
        'total_users':    total_users,
        'total_orders':   total_orders,
        'total_items':    total_items,
        'total_revenue':  total_revenue,
        'chart_labels':   labels,
        'chart_data':     data,
    }
    return render(request, 'sales/admin_dashboard.html', context)
