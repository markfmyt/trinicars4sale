import click
from flask.cli import with_appcontext
from . import db
from .models import User, Category, Product, Order, OrderItem
from datetime import datetime

def init_app(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_test_data_command)
    app.cli.add_command(init_categories_command)

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