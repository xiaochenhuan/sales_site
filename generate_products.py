# sales/management/commands/generate_products.py

from django.core.management.base import BaseCommand
from sales.models import Product
import random

class Command(BaseCommand):
    help = 'Generate 10 realistic sample products'

    SAMPLE_PRODUCTS = [
        {
            'name': 'Echo Dot (5th Gen) Smart Speaker with Alexa',
            'description': 'Our most popular smart speaker with improved bass and a sleek design, hands-free with Alexa.',
            'price': 49.99,
            'stock': 150
        },
        {
            'name': 'Instant Pot Duo 7-in-1 Electric Pressure Cooker',
            'description': 'Multi-use programmable cooker: pressure cooker, slow cooker, rice cooker, steamer, sauté, yogurt maker, and warmer.',
            'price': 89.00,
            'stock': 75
        },
        {
            'name': 'Apple AirPods Pro (2nd Generation)',
            'description': 'Active noise cancellation for immersive sound. Adaptive Transparency lets you hear the world around you.',
            'price': 249.00,
            'stock': 40
        },
        {
            'name': 'Samsung 65" Class Crystal UHD TU-8000 Series',
            'description': 'Experience TV’s next evolution in crystal clear picture quality with Crystal Processor 4K.',
            'price': 598.99,
            'stock': 25
        },
        {
            'name': 'Fitbit Charge 5 Advanced Fitness & Health Tracker',
            'description': 'Built-in GPS, Daily Readiness Score, stress management, sleep tracking, and 7-day battery life.',
            'price': 129.95,
            'stock': 100
        },
        {
            'name': 'The Silent Patient: A Novel by Alex Michaelides',
            'description': 'A shocking psychological thriller of a woman’s act of violence against her husband—and of the therapist obsessed with uncovering her motive.',
            'price': 16.20,
            'stock': 200
        },
        {
            'name': 'Le Creuset Enameled Cast Iron Signature Dutch Oven',
            'description': 'Iconic, versatile round Dutch oven features superior heat retention and distribution for all cooking methods.',
            'price': 379.00,
            'stock': 15
        },
        {
            'name': 'Logitech MX Master 3 Advanced Wireless Mouse',
            'description': 'Ergonomic design, ultra-fast scroll wheel, customizable buttons, and 70-day battery life on a full charge.',
            'price': 99.99,
            'stock': 80
        },
        {
            'name': 'Sony WH-1000XM4 Wireless Noise Cancelling Headphones',
            'description': 'Industry-leading noise cancellation, exceptional sound quality, and up to 30 hours of battery life.',
            'price': 348.00,
            'stock': 60
        },
        {
            'name': 'Ninja Professional 72oz Countertop Blender',
            'description': '1000-watt base and Total Crushing blades crush ice to snow in seconds for perfect smoothies.',
            'price': 89.99,
            'stock': 90
        },
    ]

    def handle(self, *args, **options):
        Product.objects.all().delete()
        created = []
        for item in self.SAMPLE_PRODUCTS:
            p = Product.objects.create(
                name=item['name'],
                description=item['description'],
                price=item['price'],
                stock=item['stock']
            )
            created.append(p)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(created)} products'))
