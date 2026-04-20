from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import (
    Category, Product, Banner, SiteSettings, Review
)


class Command(BaseCommand):
    help = 'Load demo data for PRIME FIT store'

    def handle(self, *args, **options):
        self.stdout.write('Loading demo data...')

        # Create categories
        categories_data = [
            {
                'name': 'T-Shirts',
                'description': 'Premium cotton t-shirts for all occasions',
                'is_active': True
            },
            {
                'name': 'Hoodies',
                'description': 'Comfortable hoodies for training and casual wear',
                'is_active': True
            },
            {
                'name': 'Jackets',
                'description': 'Performance jackets for all weather conditions',
                'is_active': True
            },
            {
                'name': 'Pants',
                'description': 'High-quality athletic pants and leggings',
                'is_active': True
            },
            {
                'name': 'Shorts',
                'description': 'Breathable shorts for intense workouts',
                'is_active': True
            },
            {
                'name': 'Accessories',
                'description': 'Training accessories and gear',
                'is_active': True
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'✓ Created category: {category.name}')

        # Create products
        products_data = [
            # T-Shirts
            {
                'category': categories['T-Shirts'],
                'name': 'Performance Training Tee',
                'description': 'Moisture-wicking fabric keeps you dry during intense workouts. Perfect for gym sessions and casual wear.',
                'price': 1299.00,
                'sale_price': 999.00,
                'gender': 'unisex',
                'available_sizes': 'XS,S,M,L,XL,XXL',
                'stock': 50,
                'is_active': True,
                'is_featured': True,
                'is_new_arrival': True
            },
            {
                'category': categories['T-Shirts'],
                'name': 'Compression Athletic Tee',
                'description': 'Advanced compression technology for muscle support and recovery. Ideal for weight training.',
                'price': 1599.00,
                'gender': 'men',
                'available_sizes': 'S,M,L,XL,XXL',
                'stock': 30,
                'is_active': True,
                'is_featured': True
            },
            {
                'category': categories['T-Shirts'],
                'name': 'Women\'s Racerback Tank',
                'description': 'Lightweight racerback design for maximum mobility. Perfect for yoga and cardio sessions.',
                'price': 899.00,
                'gender': 'women',
                'available_sizes': 'XS,S,M,L,XL',
                'stock': 40,
                'is_active': True,
                'is_new_arrival': True
            },

            # Hoodies
            {
                'category': categories['Hoodies'],
                'name': 'Premium Hooded Sweatshirt',
                'description': 'Ultra-soft fleece interior with moisture-wicking exterior. Perfect for pre and post-workout wear.',
                'price': 2499.00,
                'sale_price': 1999.00,
                'gender': 'unisex',
                'available_sizes': 'S,M,L,XL,XXL',
                'stock': 25,
                'is_active': True,
                'is_featured': True
            },
            {
                'category': categories['Hoodies'],
                'name': 'Zip-Up Training Hoodie',
                'description': 'Full-zip hoodie with thumb holes and reflective details. Great for outdoor training.',
                'price': 2799.00,
                'gender': 'unisex',
                'available_sizes': 'M,L,XL,XXL',
                'stock': 20,
                'is_active': True
            },

            # Jackets
            {
                'category': categories['Jackets'],
                'name': 'Windbreaker Jacket',
                'description': 'Lightweight wind-resistant jacket with breathable mesh panels. Perfect for running and cycling.',
                'price': 3299.00,
                'gender': 'unisex',
                'available_sizes': 'S,M,L,XL,XXL',
                'stock': 15,
                'is_active': True,
                'is_featured': True
            },
            {
                'category': categories['Jackets'],
                'name': 'Bomber Jacket',
                'description': 'Classic bomber design with modern performance fabric. Versatile for training and street wear.',
                'price': 3999.00,
                'gender': 'unisex',
                'available_sizes': 'M,L,XL',
                'stock': 12,
                'is_active': True
            },

            # Pants
            {
                'category': categories['Pants'],
                'name': 'Compression Leggings',
                'description': 'High-compression leggings for muscle support and improved circulation during workouts.',
                'price': 1899.00,
                'gender': 'unisex',
                'available_sizes': 'XS,S,M,L,XL',
                'stock': 35,
                'is_active': True,
                'is_featured': True
            },
            {
                'category': categories['Pants'],
                'name': 'Joggers',
                'description': 'Comfortable joggers with tapered fit and elastic cuffs. Perfect for casual and training wear.',
                'price': 1599.00,
                'gender': 'men',
                'available_sizes': 'S,M,L,XL,XXL',
                'stock': 28,
                'is_active': True
            },

            # Shorts
            {
                'category': categories['Shorts'],
                'name': 'Running Shorts',
                'description': 'Lightweight running shorts with built-in compression liner. Perfect for cardio sessions.',
                'price': 1199.00,
                'gender': 'unisex',
                'available_sizes': 'S,M,L,XL',
                'stock': 45,
                'is_active': True,
                'is_new_arrival': True
            },
            {
                'category': categories['Shorts'],
                'name': 'Basketball Shorts',
                'description': 'Durable basketball shorts with side pockets and moisture-wicking fabric.',
                'price': 1399.00,
                'gender': 'men',
                'available_sizes': 'M,L,XL,XXL',
                'stock': 22,
                'is_active': True
            },

            # Accessories
            {
                'category': categories['Accessories'],
                'name': 'Resistance Bands Set',
                'description': 'Complete set of resistance bands for strength training and rehabilitation. Includes 5 different resistance levels.',
                'price': 999.00,
                'gender': 'unisex',
                'available_sizes': 'One Size',
                'stock': 60,
                'is_active': True
            },
            {
                'category': categories['Accessories'],
                'name': 'Gym Gloves',
                'description': 'Premium leather gym gloves with wrist support. Perfect for weightlifting and CrossFit.',
                'price': 799.00,
                'gender': 'unisex',
                'available_sizes': 'S,M,L,XL',
                'stock': 40,
                'is_active': True
            }
        ]

        products = []
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            products.append(product)
            if created:
                self.stdout.write(f'✓ Created product: {product.name}')

        # Create banners
        banners_data = [
            {
                'title': 'TRAIN HARD',
                'subtitle': 'Elevate your performance with premium sportswear designed for champions',
                'button_text': 'Shop Now',
                'button_link': '/products/',
                'bg_color': '#0a0a0a',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'NEW ARRIVALS',
                'subtitle': 'Discover the latest in athletic wear and training gear',
                'button_text': 'Explore',
                'button_link': '/products/',
                'bg_color': '#1a1a1a',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'PERFORMANCE GEAR',
                'subtitle': 'Engineered for athletes who demand the best from their equipment',
                'button_text': 'View Collection',
                'button_link': '/products/',
                'bg_color': '#0f0f0f',
                'is_active': True,
                'order': 3
            }
        ]

        for banner_data in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            if created:
                self.stdout.write(f'✓ Created banner: {banner.title}')

        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'hero_title_line1': 'TRAIN',
                'hero_title_line2': 'HARD,',
                'hero_title_line3': 'LOOK',
                'hero_title_line4': 'ELITE',
                'hero_subtitle': 'Discover performance sportswear crafted for champions. From gym to track — gear that moves with you.',
                'hero_eyebrow': 'Premium Sports Apparel',
                'hero_btn1_text': 'Shop Collection',
                'hero_btn1_link': '/products/',
                'hero_btn2_text': 'New Arrivals',
                'hero_btn2_link': '/products/',
                'stat1_num': '12+',
                'stat1_label': 'Products',
                'stat2_num': '100%',
                'stat2_label': 'Quality',
                'stat3_num': 'XS–XXL',
                'stat3_label': 'All Sizes'
            }
        )
        if created:
            self.stdout.write('✓ Created site settings')

        # Create demo reviews
        if products and User.objects.filter(is_superuser=True).exists():
            admin_user = User.objects.filter(is_superuser=True).first()

            reviews_data = [
                {
                    'product': products[0],  # Performance Training Tee
                    'user': admin_user,
                    'rating': 5,
                    'comment': 'Excellent quality and fit! The moisture-wicking fabric really works during intense workouts.'
                },
                {
                    'product': products[1],  # Compression Athletic Tee
                    'user': admin_user,
                    'rating': 5,
                    'comment': 'Great compression support. Perfect for weight training sessions.'
                },
                {
                    'product': products[3],  # Premium Hooded Sweatshirt
                    'user': admin_user,
                    'rating': 4,
                    'comment': 'Very comfortable and warm. Good value for money with the sale price.'
                }
            ]

            for review_data in reviews_data:
                review, created = Review.objects.get_or_create(
                    product=review_data['product'],
                    user=review_data['user'],
                    defaults=review_data
                )
                if created:
                    self.stdout.write(f'✓ Created review for: {review.product.name}')

        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        self.stdout.write(f'Created {len(categories)} categories, {len(products)} products, and banners')