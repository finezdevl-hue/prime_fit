from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
import uuid
import json
from .models import (Product, Category, Banner, Cart, CartItem,
                     Order, OrderItem, Wishlist, Review, ContactMessage, SiteSettings)


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, session_key=None)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(user=None, session_key=session_key)
    return cart


def home(request):
    featured = Product.objects.filter(is_featured=True, is_active=True)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    banners = Banner.objects.filter(is_active=True)[:5]
    site_settings = SiteSettings.get_settings()
    context = {
        'featured': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'banners': banners,
        'site_settings': site_settings,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    gender = request.GET.get('gender')
    size = request.GET.get('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('q')
    sort = request.GET.get('sort', 'newest')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)
    if gender:
        products = products.filter(gender=gender)
    if size:
        products = products.filter(available_sizes__icontains=size)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'search': search,
        'sort': sort,
        'gender': gender,
        'size': size,
        'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    reviews = product.reviews.all().order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    in_wishlist = False
    user_review = None
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        user_review = Review.objects.filter(user=request.user, product=product).first()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                user=request.user, product=product,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, 'Review submitted!')
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related': related,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'in_wishlist': in_wishlist,
        'user_review': user_review,
        'sizes': product.get_sizes(),
    }
    return render(request, 'store/product_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))
    cart = get_or_create_cart(request)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size,
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'{product.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def cart_view(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    return render(request, 'store/cart.html', {'cart': cart, 'items': items})


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    action = request.POST.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    return redirect('cart')


def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        order_number = 'PF' + str(uuid.uuid4())[:8].upper()
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_number=order_number,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            payment_method=request.POST.get('payment_method', 'cod'),
            total_amount=cart.get_total(),
            notes=request.POST.get('notes', ''),
        )
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                size=item.size,
                quantity=item.quantity,
                price=item.product.get_display_price(),
            )
        cart.items.all().delete()
        return redirect('order_success', order_number=order.order_number)

    user_data = {}
    if request.user.is_authenticated:
        user_data = {'email': request.user.email,
                     'full_name': request.user.get_full_name()}
    return render(request, 'store/checkout.html', {
        'cart': cart, 'items': items, 'user_data': user_data
    })


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'Removed {product.name} from wishlist.')
    else:
        messages.success(request, f'Added {product.name} to wishlist!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1,
                first_name=first_name, last_name=last_name
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    return render(request, 'store/register.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        messages.success(request, 'Message sent! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'store/contact.html')


def about_view(request):
    return render(request, 'store/about.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile')
    return render(request, 'store/profile.html')
