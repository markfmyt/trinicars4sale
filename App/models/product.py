from .. import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    series = db.Column(db.String(50))
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer)
    transmission = db.Column(db.String(20))
    fuel_type = db.Column(db.String(20))
    color = db.Column(db.String(30))
    contact_number = db.Column(db.String(20))
    is_negotiable = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    listing_tier = db.Column(db.String(20), default='standard')
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image_url': self.image_url,
            'category_id': self.category_id,
            'seller_id': self.seller_id,
            'make': self.make,
            'model': self.model,
            'series': self.series,
            'year': self.year,
            'mileage': self.mileage,
            'transmission': self.transmission,
            'fuel_type': self.fuel_type,
            'color': self.color,
            'contact_number': self.contact_number,
            'is_negotiable': self.is_negotiable,
            'is_premium': self.is_premium,
            'is_featured': self.is_featured,
            'listing_tier': self.listing_tier,
            'views': self.views,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 