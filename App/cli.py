import click
from flask.cli import with_appcontext
from . import db
from .models import User, Category, Product, Order, OrderItem
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_app(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_test_data_command)
    app.cli.add_command(init_categories_command)
    app.cli.add_command(init_sample_data_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

@click.command('create-admin')
@with_appcontext
def create_admin_command():
    """Create an admin user."""
    username = click.prompt('Enter admin username')
    email = click.prompt('Enter admin email')
    password = click.prompt('Enter admin password', hide_input=True, confirmation_prompt=True)
    
    if User.query.filter_by(username=username).first():
        click.echo('Username already exists.')
        return
    
    if User.query.filter_by(email=email).first():
        click.echo('Email already exists.')
        return
    
    user = User(username=username, email=email, password=password)
    user.is_admin = True
    db.session.add(user)
    db.session.commit()
    click.echo('Admin user created successfully.')

@click.command('init-categories')
@with_appcontext
def init_categories_command():
    """Initialize default categories."""
    categories = [
        Category(name='Sedan', description='Four-door passenger cars'),
        Category(name='SUV', description='Sport Utility Vehicles'),
        Category(name='Truck', description='Pickup trucks and commercial vehicles'),
        Category(name='Van', description='Passenger and cargo vans'),
        Category(name='Sports Car', description='High-performance vehicles'),
        Category(name='Electric', description='Electric and hybrid vehicles'),
        Category(name='Luxury', description='High-end luxury vehicles'),
        Category(name='Classic', description='Vintage and classic cars')
    ]
    
    for category in categories:
        if not Category.query.filter_by(name=category.name).first():
            db.session.add(category)
    
    db.session.commit()
    click.echo('Initialized categories.')

@click.command('init-test-data')
@with_appcontext
def init_test_data_command():
    """Initialize test data."""
    # Create admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password='admin123',
        is_admin=True,
        is_verified=True
    )
    db.session.add(admin)
    
    # Create regular user
    user = User(
        username='user',
        email='user@example.com',
        password='user123',
        is_verified=True
    )
    db.session.add(user)
    
    # Create categories if they don't exist
    categories = [
        Category(name='Sedan', description='Four-door passenger cars'),
        Category(name='SUV', description='Sport Utility Vehicles'),
        Category(name='Truck', description='Pickup trucks and commercial vehicles'),
        Category(name='Van', description='Passenger and cargo vans'),
        Category(name='Sports Car', description='High-performance vehicles'),
        Category(name='Electric', description='Electric and hybrid vehicles'),
        Category(name='Luxury', description='High-end luxury vehicles'),
        Category(name='Classic', description='Vintage and classic cars')
    ]
    
    for category in categories:
        if not Category.query.filter_by(name=category.name).first():
            db.session.add(category)
    
    db.session.commit()
    
    # Create some test products
    products = [
        Product(
            name='Toyota Camry',
            description='A reliable and comfortable sedan',
            price=25000.00,
            stock=1,
            image_url='uploads/car (1).jpg',
            category_id=1,  # Sedan
            seller_id=1,    # admin
            make='Toyota',
            model='Camry',
            year=2020,
            mileage=15000,
            transmission='Automatic',
            fuel_type='Gasoline',
            color='Silver'
        ),
        Product(
            name='Honda CR-V',
            description='Popular SUV with great fuel economy',
            price=30000.00,
            stock=1,
            image_url='uploads/car (2).jpg',
            category_id=2,  # SUV
            seller_id=2,    # user
            make='Honda',
            model='CR-V',
            year=2021,
            mileage=10000,
            transmission='Automatic',
            fuel_type='Gasoline',
            color='Black'
        )
    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    click.echo('Initialized test data.')

@click.command('init-sample-data')
@with_appcontext
def init_sample_data_command():
    """Initialize sample data for demonstration."""
    # Create categories if they don't exist
    categories = {
        'Sports Car': Category.query.filter_by(name='Sports Car').first() or Category(name='Sports Car'),
        'Electric': Category.query.filter_by(name='Electric').first() or Category(name='Electric'),
        'Sedan': Category.query.filter_by(name='Sedan').first() or Category(name='Sedan'),
        'Luxury': Category.query.filter_by(name='Luxury').first() or Category(name='Luxury')
    }
    
    for category in categories.values():
        if not category.id:
            db.session.add(category)
    
    # Create Mark's user account
    mark = User.query.filter_by(email='mark@mail.com').first()
    if not mark:
        mark = User(
            username='mark',
            email='mark@mail.com',
            password='1',
            phone='+1-868-123-4567'
        )
        db.session.add(mark)
    
    # Commit to get user ID
    db.session.commit()
    
    # Create listings
    listings = [
        {
            'name': 'Lamborghini Murciélago',
            'price': 1904000,
            'description': 'A stunning blue Lamborghini Murciélago LP640 with scissor doors and a powerful V12 engine. Iconic design and top-tier performance.',
            'make': 'Lamborghini',
            'model': 'Murciélago',
            'series': 'LP640',
            'year': 2008,
            'mileage': 22000,
            'transmission': 'Automatic',
            'fuel_type': 'Gasoline',
            'color': 'Blue',
            'category_id': categories['Sports Car'].id,
            'listing_tier': 'Premium',
            'seller_id': mark.id,
            'stock': 1,
            'image_url': 'images/lamborghini.png',
            'contact_number': '+1-868-123-4567',
            'is_negotiable': False,
            'is_premium': True,
            'is_featured': False
        },
        {
            'name': 'Tesla Cybertruck AWD',
            'price': 510000,
            'description': 'All-electric Tesla Cybertruck with futuristic design and exceptional off-road capability. Stainless steel exoskeleton.',
            'make': 'Tesla',
            'model': 'Cybertruck',
            'series': 'AWD',
            'year': 2024,
            'mileage': 500,
            'transmission': 'Automatic',
            'fuel_type': 'Electric',
            'color': 'Silver',
            'category_id': categories['Electric'].id,
            'listing_tier': 'Featured',
            'seller_id': mark.id,
            'stock': 1,
            'image_url': 'images/cybertruck.png',
            'contact_number': '+1-868-123-4567',
            'is_negotiable': False,
            'is_premium': False,
            'is_featured': True
        },
        {
            'name': 'Mitsubishi Lancer Evo IX',
            'price': 258400,
            'description': 'Tuned Mitsubishi Lancer Evolution IX. Turbocharged performance with rally heritage. Clean and sharp white exterior.',
            'make': 'Mitsubishi',
            'model': 'Lancer',
            'series': 'Evolution IX',
            'year': 2006,
            'mileage': 78000,
            'transmission': 'Manual',
            'fuel_type': 'Gasoline',
            'color': 'White',
            'category_id': categories['Sedan'].id,
            'listing_tier': 'Standard',
            'seller_id': mark.id,
            'stock': 1,
            'image_url': 'images/lancer.png',
            'contact_number': '+1-868-123-4567',
            'is_negotiable': True,
            'is_premium': False,
            'is_featured': True
        },
        {
            'name': 'Mercedes-AMG S63',
            'price': 1258000,
            'description': 'Luxurious and powerful Mercedes-AMG S63 with 4MATIC+ and V8 Biturbo engine. Black on black styling.',
            'make': 'Mercedes-Benz',
            'model': 'S-Class',
            'series': 'AMG S63',
            'year': 2023,
            'mileage': 12000,
            'transmission': 'Automatic',
            'fuel_type': 'Gasoline',
            'color': 'Black',
            'category_id': categories['Luxury'].id,
            'listing_tier': 'Featured',
            'seller_id': mark.id,
            'stock': 1,
            'image_url': 'images/mercedes.png',
            'contact_number': '+1-868-123-4567',
            'is_negotiable': False,
            'is_premium': False,
            'is_featured': True
        }
    ]
    
    # Add listings if they don't exist
    for listing_data in listings:
        existing_listing = Product.query.filter_by(
            name=listing_data['name'],
            seller_id=mark.id
        ).first()
        
        if not existing_listing:
            listing = Product(**listing_data)
            db.session.add(listing)
    
    db.session.commit()
    click.echo('Initialized sample data for Mark\'s account') 