# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///urls.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'

# app.py
from flask import Flask, request, jsonify, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_clicked = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_clicked': self.last_clicked.strftime('%Y-%m-%d %H:%M:%S') if self.last_clicked else None
        }

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/')
def index():
    recent_urls = URL.query.order_by(URL.created_at.desc()).limit(10).all()
    return render_template('index.html', urls=recent_urls)

@app.route('/stats/<short_code>')
def stats_page(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first_or_404()
    return render_template('stats.html', url=url_data)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
        
    original_url = data['url']
    
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url
    
    existing_url = URL.query.filter_by(original_url=original_url).first()
    if existing_url:
        return jsonify(existing_url.to_dict())
    
    short_code = generate_short_code()
    new_url = URL(original_url=original_url, short_code=short_code)
    
    db.session.add(new_url)
    db.session.commit()
    
    return jsonify(new_url.to_dict())

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url
