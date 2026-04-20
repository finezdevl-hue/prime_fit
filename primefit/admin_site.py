from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from store.models import Order, Product, ContactMessage


class PrimeFitAdminSite(AdminSite):
    site_header = '⚡ PRIME FIT Apparels Admin'
    site_title = 'PRIME FIT Admin'
    index_title = 'Dashboard'
    index_template = 'admin/index.html'
    login_template = 'admin/login.html'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_orders'] = Order.objects.count()
        extra_context['total_products'] = Product.objects.filter(is_active=True).count()
        extra_context['total_users'] = User.objects.filter(is_staff=False).count()
        extra_context['unread_msgs'] = ContactMessage.objects.filter(is_read=False).count()
        return super().index(request, extra_context)
