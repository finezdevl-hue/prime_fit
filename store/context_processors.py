from .models import Cart, Category


def cart_count(request):
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            if request.session.session_key:
                cart = Cart.objects.filter(session_key=request.session.session_key, user=None).first()
            else:
                cart = None
        if cart:
            count = cart.get_count()
    except Exception:
        pass
    categories = Category.objects.filter(is_active=True)
    return {'cart_count': count, 'nav_categories': categories}
