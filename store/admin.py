from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import (Category, Product, Banner, Cart, CartItem,
                     Order, OrderItem, Wishlist, Review, ContactMessage, SiteSettings)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        count = obj.products.filter(is_active=True).count()
        return format_html('<span style="color:#C9A227;font-weight:bold">{}</span>', count)
    product_count.short_description = 'Products'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'size', 'quantity', 'price', 'subtotal']
    fields = ['product_name', 'size', 'quantity', 'price', 'subtotal']

    def subtotal(self, obj):
        amount = '{:,.2f}'.format(float(obj.get_subtotal()))
        return format_html('₹{}', amount)
    subtotal.short_description = 'Subtotal'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_image', 'name', 'category', 'price', 'sale_price',
                    'stock', 'gender', 'is_active', 'is_featured', 'is_new_arrival']
    list_filter = ['category', 'gender', 'is_active', 'is_featured', 'is_new_arrival']
    search_fields = ['name', 'description']
    list_editable = ['price', 'sale_price', 'stock', 'is_active', 'is_featured', 'is_new_arrival']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['product_preview']
    list_per_page = 20

    fieldsets = (
        ('Basic Info', {'fields': ('name', 'slug', 'category', 'description', 'gender')}),
        ('Pricing & Stock', {'fields': ('price', 'sale_price', 'stock', 'available_sizes')}),
        ('Images', {'fields': ('image', 'product_preview', 'image2', 'image3')}),
        ('Visibility', {'fields': ('is_active', 'is_featured', 'is_new_arrival')}),
    )

    def product_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;">', obj.image.url)
        return format_html('<div style="width:50px;height:50px;background:#1a1a1a;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#C9A227">PF</div>')
    product_image.short_description = 'Image'

    def product_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px;border-radius:12px;">', obj.image.url)
        return 'No image'
    product_preview.short_description = 'Preview'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_preview', 'title', 'subtitle', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    search_fields = ['title']
    readonly_fields = ['banner_preview_large']

    fieldsets = (
        ('Banner Content', {
            'description': 'Upload an image for the banner slider on the homepage. '
                           'Recommended size: 1400×500px. If no image is uploaded, '
                           'a styled text banner is shown instead.',
            'fields': ('title', 'subtitle', 'button_text', 'button_link')
        }),
        ('Image & Style', {
            'fields': ('image', 'banner_preview_large', 'bg_color')
        }),
        ('Visibility', {
            'fields': ('is_active', 'order')
        }),
    )

    def banner_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:90px;height:40px;object-fit:cover;border-radius:6px;border:2px solid #C9A227">',
                obj.image.url
            )
        return format_html(
            '<div style="width:90px;height:40px;background:{};border-radius:6px;display:flex;align-items:center;'
            'justify-content:center;font-size:10px;color:#C9A227;border:1px dashed #C9A227">No Image</div>',
            obj.bg_color
        )
    banner_preview.short_description = 'Preview'

    def banner_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:500px;max-height:180px;object-fit:cover;border-radius:10px;'
                'border:2px solid #C9A227;margin-top:6px">',
                obj.image.url
            )
        return format_html(
            '<div style="padding:12px;background:#1a1a1a;border-radius:8px;color:#888;font-size:12px;">'
            '📷 No image uploaded yet. Upload an image above (recommended: 1400×500px)</div>'
        )
    banner_preview_large.short_description = 'Current Banner Preview'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'total_badge',
                    'payment_method', 'status', 'status_badge', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'full_name', 'email', 'phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    list_per_page = 20

    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'status', 'payment_method', 'total_amount', 'notes')}),
        ('Customer', {'fields': ('user', 'full_name', 'email', 'phone')}),
        ('Shipping', {'fields': ('address', 'city', 'state', 'pincode')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def total_badge(self, obj):
        amount = '{:,.2f}'.format(float(obj.total_amount))
        return format_html('<strong style="color:#C9A227">₹{}</strong>', amount)
    total_badge.short_description = 'Total'

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b', 'confirmed': '#3b82f6', 'processing': '#8b5cf6',
            'shipped': '#06b6d4', 'delivered': '#10b981', 'cancelled': '#ef4444'
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:bold">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'product__name']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']

    def has_add_permission(self, request):
        return False


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_at']
    list_filter = ['added_at']



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ['hero_image_preview']

    fieldsets = (
        ('🖼️ Hero Image', {
            'description': 'Upload a full-resolution image for the homepage hero section. '
                           'Recommended: 1920×1080px or taller portrait image. '
                           'The image appears on the RIGHT side of the hero behind a dark overlay.',
            'fields': ('hero_image', 'hero_image_preview'),
        }),
        ('📝 Hero Text', {
            'fields': (
                'hero_eyebrow',
                'hero_title_line1', 'hero_title_line2',
                'hero_title_line3', 'hero_title_line4',
                'hero_subtitle',
            ),
        }),
        ('🔘 Hero Buttons', {
            'fields': ('hero_btn1_text', 'hero_btn1_link', 'hero_btn2_text', 'hero_btn2_link'),
        }),
        ('📊 Stats Bar', {
            'fields': (
                'stat1_num', 'stat1_label',
                'stat2_num', 'stat2_label',
                'stat3_num', 'stat3_label',
            ),
        }),
    )

    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="max-width:500px;max-height:220px;object-fit:cover;'
                'border-radius:12px;border:2px solid #C9A227;margin-top:8px">',
                obj.hero_image.url
            )
        return format_html(
            '<div style="padding:16px;background:#1a1a1a;border-radius:10px;color:#888;font-size:13px;'
            'border:1px dashed #C9A227;margin-top:8px">'
            '📷 No hero image uploaded yet.<br>'
            '<span style="color:#C9A227">Upload an image above</span> — recommended size: <strong style="color:#fff">1920×1080px</strong></div>'
        )
    hero_image_preview.short_description = 'Current Hero Image Preview'

    def has_add_permission(self, request):
        # Allow add only if no settings exist yet
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent accidental deletion


# Custom Admin Site Styling
admin.site.site_header = format_html(
    '<span style="color:#C9A227;font-family:Georgia,serif;letter-spacing:2px">⚡ PRIME FIT</span> '
    '<span style="color:#fff;font-size:14px">Admin Panel</span>'
)
