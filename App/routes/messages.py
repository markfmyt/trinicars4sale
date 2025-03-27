from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Message, Product, User
from datetime import datetime

bp = Blueprint('messages', __name__)

@bp.route('/messages')
@login_required
def get_messages():
    """Get all messages for the current user"""
    # Get query parameters for direct messaging
    seller_username = request.args.get('seller')
    product_id = request.args.get('product')
    
    # If direct messaging parameters are present, show the message form
    show_message_form = False
    recipient = None
    product = None
    
    if seller_username and product_id:
        recipient = User.query.filter_by(username=seller_username).first()
        product = Product.query.get(product_id)
        if recipient and product:
            show_message_form = True
    
    # Get all messages
    received_messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.created_at.desc()).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    return render_template('messages/index.html',
                         received_messages=received_messages,
                         sent_messages=sent_messages,
                         show_message_form=show_message_form,
                         recipient=recipient,
                         product=product)

@bp.route('/messages/send', methods=['POST'])
@login_required
def send_message():
    """Send a message to another user"""
    recipient_id = request.form.get('recipient_id')
    product_id = request.form.get('product_id')
    content = request.form.get('content')
    
    if not all([recipient_id, content]):
        flash('Message cannot be empty', 'error')
        return redirect(url_for('messages.get_messages'))
    
    # Create and save the message
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        product_id=product_id,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    
    flash('Message sent successfully!', 'success')
    return redirect(url_for('messages.get_messages'))

@bp.route('/messages/<int:message_id>/read', methods=['POST'])
@login_required
def mark_as_read(message_id):
    """Mark a message as read"""
    message = Message.query.get_or_404(message_id)
    
    if message.recipient_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    message.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})

@bp.route('/messages/unread')
@login_required
def get_unread_count():
    """Get the count of unread messages"""
    count = Message.query.filter_by(recipient_id=current_user.id, is_read=False).count()
    return jsonify({'count': count}) 