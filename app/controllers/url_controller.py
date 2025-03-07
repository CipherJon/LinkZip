from flask import Blueprint, request, jsonify, redirect
from datetime import datetime
from app.models.url_model import Url
from app.utils.generate_code import generate_short_code
from app import db

url_controller = Blueprint('url', __name__)

@url_controller.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.json
    original_url = data.get('url')
    user_id = data.get('user_id')  # Assuming authentication system provides this
    
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        short_code = generate_short_code()
        expires_at = data.get('expires_at')  # Expect ISO format string from client
        
        url_entry = Url(
            original_url=original_url,
            short_code=short_code,
            clicks=0,
            user_id=user_id,
            expires_at=datetime.fromisoformat(expires_at) if expires_at else None
        )
        
        db.session.add(url_entry)
        db.session.commit()
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Database error'}), 500

    return jsonify({
        'original_url': original_url,
        'short_url': f'{request.host_url}{short_code}',
        'expires_at': url_entry.expires_at.isoformat() if url_entry.expires_at else None
    }), 201

@url_controller.route('/<short_code>', methods=['GET'])
def redirect_to_original_url(short_code):
    url_entry = Url.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'Short URL not found'}), 404
        
    if url_entry.expires_at and url_entry.expires_at < datetime.utcnow():
        return jsonify({'error': 'This short URL has expired'}), 410
    
    try:
        url_entry.clicks += 1
        url_entry.last_accessed = datetime.utcnow()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update URL stats'}), 500
    
    return redirect(url_entry.original_url)

@url_controller.route('/<short_code>/stats', methods=['GET'])
def get_url_analytics(short_code):
    url_entry = Url.query.filter_by(short_code=short_code).first()
    
    if not url_entry:
        return jsonify({'error': 'Short URL not found'}), 404
    
    return jsonify({
        'original_url': url_entry.original_url,
        'short_code': url_entry.short_code,
        'clicks': url_entry.clicks,
        'created_at': url_entry.created_at.isoformat(),
        'expires_at': url_entry.expires_at.isoformat() if url_entry.expires_at else None,
        'last_accessed': url_entry.last_accessed.isoformat() if url_entry.last_accessed else None,
        'user_id': url_entry.user_id
    })