from app import db
from datetime import datetime
from sqlalchemy.orm import validates

class Url(db.Model):
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='urls')

    @validates('original_url')
    def validate_url(self, key, url):
        """Validate URL format using basic pattern check"""
        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        return url

    @validates('short_code')
    def validate_short_code(self, key, code):
        """Ensure short code contains only alphanumeric characters"""
        if not code.isalnum():
            raise ValueError("Short code must be alphanumeric")
        return code

    def __repr__(self):
        return f"<Url {self.short_code} - {self.original_url}>"