# app.py
from flask import Flask, request, jsonify, redirect, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import re
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ''  # Change this in production

db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_clicked = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    ip_address = db.Column(db.String(45))  # Store creator's IP address

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_clicked': self.last_clicked.strftime('%Y-%m-%d %H:%M:%S') if self.last_clicked else None,
            'is_active': self.is_active
        }

class ClickLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    referrer = db.Column(db.String(200))

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    urls = URL.query.order_by(URL.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('index.html', urls=urls)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
        
    original_url = data['url']
    
    # Add http:// if no protocol specified
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url
    
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    # Check for existing URL
    existing_url = URL.query.filter_by(original_url=original_url, is_active=True).first()
    if existing_url:
        return jsonify(existing_url.to_dict())
    
    try:
        short_code = generate_short_code()
        new_url = URL(
            original_url=original_url,
            short_code=short_code,
            ip_address=request.remote_addr
        )
        
        db.session.add(new_url)
        db.session.commit()
        
        return jsonify(new_url.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while shortening the URL'}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_data = URL.query.filter_by(short_code=short_code, is_active=True).first_or_404()
    
    # Log the click
    click_log = ClickLog(
        url_id=url_data.id,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        referrer=request.referrer
    )
    
    url_data.clicks += 1
    url_data.last_clicked = datetime.utcnow()
    
    try:
        db.session.add(click_log)
        db.session.commit()
    except:
        db.session.rollback()
        # Continue with redirect even if logging fails
    
    return redirect(url_data.original_url)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    url_data = URL.query.filter_by(short_code=short_code, is_active=True).first_or_404()
    
    clicks_by_day = db.session.query(
        db.func.date(ClickLog.clicked_at).label('date'),
        db.func.count(ClickLog.id).label('clicks')
    ).filter(ClickLog.url_id == url_data.id)\
     .group_by(db.func.date(ClickLog.clicked_at))\
     .all()
    
    stats = url_data.to_dict()
    stats['clicks_by_day'] = [{'date': str(day), 'clicks': clicks} for day, clicks in clicks_by_day]
    
    return jsonify(stats)

@app.route('/api/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first_or_404()
    
    # Soft delete
    url_data.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'URL deactivated successfully'})
    except:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deactivating the URL'}), 500

@app.errorhandler(404)
def
