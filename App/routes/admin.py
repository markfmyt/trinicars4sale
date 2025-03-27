from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import User, Category, Product, Order, OrderItem
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat()
    } for user in users])

@bp.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'username' in data:
        if User.query.filter_by(username=data['username']).first() and data['username'] != user.username:
            return jsonify({'error': 'Username already taken'}), 400
        user.username = data['username']
    
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({'error': 'Email already registered'}), 400
        user.email = data['email']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat()
    })

@bp.route('/categories', methods=['GET'])
@admin_required
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description
    } for c in categories])

@bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json()
    
    if Category.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Category name already exists'}), 400
    
    category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    }), 201

@bp.route('/categories/<int:id>', methods=['PUT'])
@admin_required
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        if Category.query.filter_by(name=data['name']).first() and data['name'] != category.name:
            return jsonify({'error': 'Category name already exists'}), 400
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

@bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    # Get total users
    total_users = User.query.count()
    
    # Get total products
    total_products = Product.query.count()
    
    # Get total orders
    total_orders = Order.query.count()
    
    # Get total revenue
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
    
    # Get recent orders (last 7 days)
    recent_orders = Order.query.filter(
        Order.created_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    # Get top products by sales
    top_products = db.session.query(
        Product,
        func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
    
    return jsonify({
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': float(total_revenue),
        'recent_orders': [{
            'id': order.id,
            'user_id': order.user_id,
            'total_amount': order.total_amount,
            'status': order.status,
            'created_at': order.created_at.isoformat()
        } for order in recent_orders],
        'top_products': [{
            'id': product.id,
            'name': product.name,
            'total_sold': total_sold
        } for product, total_sold in top_products]
    }) 