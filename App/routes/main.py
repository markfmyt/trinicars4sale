from flask import Blueprint, render_template
from ..models import Product

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    featured_products = Product.query.limit(96).all()
    return render_template('index.html', featured_products=featured_products)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html') 