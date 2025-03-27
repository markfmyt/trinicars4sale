from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models import Order, OrderItem, Product, User
from datetime import datetime

bp = Blueprint('orders', __name__)

@bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in data['items']:
        product = Product.query.get_or_404(item['product_id'])
        if product.stock < item['quantity']:
            return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
        
        total_amount += product.price * item['quantity']
        order_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': product.price
        })
    
    # Create order
    order = Order(
        user_id=current_user_id,
        total_amount=total_amount,
        status='pending'
    )
    db.session.add(order)
    
    # Create order items and update stock
    for item in order_items:
        order_item = OrderItem(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )
        item['product'].stock -= item['quantity']
        db.session.add(order_item)
    
    db.session.commit()
    
    return jsonify({
        'id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat()
    }), 201

@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    } for order in orders])

@bp.route('/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    order = Order.query.get_or_404(id)
    
    if not user.is_admin and order.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    })

@bp.route('/orders/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = Order.query.get_or_404(id)
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    order.status = data['status']
    db.session.commit()
    
    return jsonify({
        'id': order.id,
        'status': order.status,
        'updated_at': order.updated_at.isoformat()
    }) 