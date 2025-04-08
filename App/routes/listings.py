from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .. import db
from ..models import Product, Category
from datetime import datetime

bp = Blueprint('listings', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@bp.route('/listings')
def get_listings():
    page = request.args.get('page', 1, type=int)
    make = request.args.get('make')
    model = request.args.get('model')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    year = request.args.get('year', type=int)
    
    query = Product.query
    
    if make:
        query = query.filter(Product.make.ilike(f'%{make}%'))
    if model:
        query = query.filter(Product.model.ilike(f'%{model}%'))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if year:
        query = query.filter(Product.year == year)
    
    # Show premium listings first
    query = query.order_by(Product.is_premium.desc(), Product.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=12, error_out=False)
    products = pagination.items
    
    categories = Category.query.all()
    makes = db.session.query(Product.make).distinct().all()
    years = db.session.query(Product.year).distinct().order_by(Product.year.desc()).all()
    
    return render_template('listings/index.html', 
                         products=products, 
                         pagination=pagination,
                         categories=categories,
                         makes=makes,
                         years=years)

@bp.route('/listings/new', methods=['GET', 'POST'])
@login_required
def create_listing():
    if request.method == 'GET':
        categories = Category.query.all()
        print("Available categories:", [{"id": c.id, "name": c.name} for c in categories])  # Debug print
        if not categories:
            # If no categories exist, create them
            default_categories = [
                Category(name='Sedan', description='Four-door passenger cars'),
                Category(name='SUV', description='Sport Utility Vehicles'),
                Category(name='Truck', description='Pickup trucks and commercial vehicles'),
                Category(name='Van', description='Passenger and cargo vans'),
                Category(name='Sports Car', description='High-performance vehicles'),
                Category(name='Electric', description='Electric and hybrid vehicles'),
                Category(name='Luxury', description='High-end luxury vehicles'),
                Category(name='Classic', description='Vintage and classic cars')
            ]
            for category in default_categories:
                db.session.add(category)
            db.session.commit()
            categories = Category.query.all()
            print("Created default categories:", [{"id": c.id, "name": c.name} for c in categories])  # Debug print
        return render_template('listings/create.html', categories=categories, now=datetime.now())
    
    # Handle form submission
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))
    make = request.form.get('make')
    model = request.form.get('model')
    series = request.form.get('series')
    year = int(request.form.get('year'))
    mileage = request.form.get('mileage', type=int)
    transmission = request.form.get('transmission')
    fuel_type = request.form.get('fuel_type')
    color = request.form.get('color')
    category_id = int(request.form.get('category_id'))
    contact_number = request.form.get('contact_number')
    is_negotiable = bool(request.form.get('is_negotiable'))
    listing_tier = request.form.get('listing_tier', 'standard')
    
    # Set premium and featured flags based on tier
    is_premium = listing_tier == 'premium'
    is_featured = listing_tier in ['premium', 'featured']
    
    # Handle image upload
    image = request.files.get('image')
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_url = f"uploads/{filename}"
    else:
        flash('Invalid image file', 'error')
        return redirect(url_for('listings.create_listing'))
    
    product = Product(
        name=name,
        description=description,
        price=price,
        stock=1,  # Since it's a single vehicle
        image_url=image_url,
        category_id=category_id,
        seller_id=current_user.id,
        make=make,
        model=model,
        series=series,
        year=year,
        mileage=mileage,
        transmission=transmission,
        fuel_type=fuel_type,
        color=color,
        contact_number=contact_number,
        is_negotiable=is_negotiable,
        is_premium=is_premium,
        is_featured=is_featured,
        listing_tier=listing_tier
    )
    
    db.session.add(product)
    db.session.commit()
    
    flash('Listing created successfully!', 'success')
    return redirect(url_for('listings.get_listing', id=product.id))

@bp.route('/listings/<int:id>')
def get_listing(id):
    product = Product.query.get_or_404(id)
    product.views += 1
    db.session.commit()
    return render_template('listings/detail.html', product=product)

@bp.route('/listings/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_listing(id):
    product = Product.query.get_or_404(id)
    
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this listing.', 'error')
        return redirect(url_for('listings.get_listing', id=id))
    
    if request.method == 'GET':
        categories = Category.query.all()
        return render_template('listings/edit.html', product=product, categories=categories, now=datetime.now())
    
    # Handle form submission
    product.name = request.form.get('name')
    product.description = request.form.get('description')
    product.price = float(request.form.get('price'))
    product.make = request.form.get('make')
    product.model = request.form.get('model')
    product.year = int(request.form.get('year'))
    product.mileage = request.form.get('mileage', type=int)
    product.transmission = request.form.get('transmission')
    product.fuel_type = request.form.get('fuel_type')
    product.color = request.form.get('color')
    product.category_id = int(request.form.get('category_id'))
    
    # Handle listing tier update
    listing_tier = request.form.get('listing_tier', 'standard')
    product.listing_tier = listing_tier
    product.is_premium = listing_tier == 'premium'
    product.is_featured = listing_tier in ['premium', 'featured']
    
    # Handle image upload if new image is provided
    image = request.files.get('image')
    if image and allowed_file(image.filename):
        # Delete old image
        if product.image_url:
            old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1])
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        
        filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        product.image_url = f"uploads/{filename}"
    
    db.session.commit()
    flash('Listing updated successfully!', 'success')
    return redirect(url_for('listings.get_listing', id=id))

@bp.route('/listings/<int:id>/delete', methods=['POST'])
@login_required
def delete_listing(id):
    product = Product.query.get_or_404(id)
    
    if product.seller_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this listing.', 'error')
        return redirect(url_for('listings.get_listing', id=id))
    
    # Delete image file
    if product.image_url:
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], product.image_url.split('/')[-1])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Listing deleted successfully!', 'success')
    return redirect(url_for('listings.get_listings')) 