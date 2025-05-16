import random
from django.core.management.base import BaseCommand
from sales.models import Product
from faker import Faker

# Initialize Faker
fake = Faker()

# Category and adjective pools for product name generation
CATEGORIES = [
    'Wireless Earbuds', 'Bluetooth Speaker', 'Smartwatch',
    'Gaming Keyboard', '4K Monitor', 'USB-C Hub',
    'Coffee Maker', 'Air Fryer', 'Electric Toothbrush',
    'Yoga Mat', 'Running Shoes', 'Water Bottle',
    'Backpack', 'Travel Pillow', 'LED Desk Lamp',
    'Portable Charger', 'Action Camera', 'Noise Cancelling Headphones',
    'Smart Thermostat', 'Robot Vacuum'
]

ADJECTIVES = [
    'Advanced', 'Premium', 'Ultra', 'Compact', 'Lightweight',
    'Ergonomic', 'Rechargeable', 'Multi-purpose', 'High-speed',
    'Durable', 'Waterproof', 'Eco-friendly', 'Wireless', 'Automatic'
]

# Generate 1000 realistic sample products
SAMPLE_PRODUCTS = []
for _ in range(1000):
    category = random.choice(CATEGORIES)
    adjective = random.choice(ADJECTIVES)
    model = fake.bothify(text='??###').upper()
    name = f"{adjective} {category} {model}"

    # Build a 2-3 sentence description
    desc_sentences = [
        fake.sentence(nb_words=8),
        fake.sentence(nb_words=10),
        fake.sentence(nb_words=12)
    ]
    description = " ".join(desc_sentences)

    price = round(random.uniform(15.00, 499.99), 2)
    stock = random.randint(10, 500)

    SAMPLE_PRODUCTS.append({
        'name': name,
        'description': description,
        'price': price,
        'stock': stock
    })

class Command(BaseCommand):
    help = 'Generate 1000 realistic sample products'

    def handle(self, *args, **options):
        # Clear existing products
        Product.objects.all().delete()
        created = []

        # Create new products
        for item in SAMPLE_PRODUCTS:
            p = Product.objects.create(
                name=item['name'],
                description=item['description'],
                price=item['price'],
                stock=item['stock']
            )
            created.append(p)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created)} products'
            )
        )