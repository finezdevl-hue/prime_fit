from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


SIZE_CHOICES = [
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
]

GENDER_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('unisex', 'Unisex'),
    ('kids', 'Kids'),
]


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    available_sizes = models.CharField(max_length=50, default='XS,S,M,L,XL,XXL',
                                       help_text='Comma separated: XS,S,M,L,XL,XXL')
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_sizes(self):
        return [s.strip() for s in self.available_sizes.split(',') if s.strip()]

    def get_discount_percent(self):
        if self.sale_price and self.price > 0:
            discount = ((self.price - self.sale_price) / self.price) * 100
            return int(discount)
        return 0

    def get_display_price(self):
        return self.sale_price if self.sale_price else self.price

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    button_text = models.CharField(max_length=50, default='Shop Now')
    button_link = models.CharField(max_length=200, default='/')
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    bg_color = models.CharField(max_length=20, default='#0a0a0a')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

    def get_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart ({self.user or self.session_key})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, default='M')
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        if not self.product:
            return 0
        return (self.product.get_display_price() or 0) * (self.quantity or 0)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} ({self.size})"


ORDER_STATUS = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

PAYMENT_METHOD = [
    ('cod', 'Cash on Delivery'),
    ('upi', 'UPI'),
    ('card', 'Credit/Debit Card'),
    ('netbanking', 'Net Banking'),
]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cod')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    size = models.CharField(max_length=5)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        price = self.price or 0
        quantity = self.quantity or 0
        return price * quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSettings(models.Model):
    """Singleton model — only one row should exist. Edit via Admin."""
    # Hero Section
    hero_image = models.ImageField(
        upload_to='hero/',
        blank=True, null=True,
        help_text='Recommended size: 1920x1080px. Appears on the right side of the homepage hero.'
    )
    hero_title_line1 = models.CharField(max_length=50, default='TRAIN', help_text='First line of hero heading')
    hero_title_line2 = models.CharField(max_length=50, default='HARD,', help_text='Second line (gold colour)')
    hero_title_line3 = models.CharField(max_length=50, default='LOOK', help_text='Third line')
    hero_title_line4 = models.CharField(max_length=50, default='ELITE', help_text='Fourth line (gold colour)')
    hero_subtitle    = models.CharField(
        max_length=200,
        default='Discover performance sportswear crafted for champions. From gym to track — gear that moves with you.'
    )
    hero_eyebrow = models.CharField(max_length=100, default='Premium Sports Apparel')
    hero_btn1_text = models.CharField(max_length=40, default='Shop Collection')
    hero_btn1_link = models.CharField(max_length=200, default='/products/')
    hero_btn2_text = models.CharField(max_length=40, default='New Arrivals')
    hero_btn2_link = models.CharField(max_length=200, default='/products/')
    # Stats
    stat1_num   = models.CharField(max_length=20, default='500+')
    stat1_label = models.CharField(max_length=30, default='Products')
    stat2_num   = models.CharField(max_length=20, default='5K+')
    stat2_label = models.CharField(max_length=30, default='Happy Customers')
    stat3_num   = models.CharField(max_length=20, default='XS–XXL')
    stat3_label = models.CharField(max_length=30, default='All Sizes')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'PRIME FIT Site Settings'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
