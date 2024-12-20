# app.py
from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'clicks': self.clicks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

@app.route('/')
def index():
    urls = URL.query.order_by(URL.created_at.desc()).limit(10).all()
    return render_template('index.html', urls=urls)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
        
    original_url = data['url']
    
    # Basic URL validation
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url
    
    # Check if URL already exists
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
    url_data = URL.query.filter_by(short_code=short_code).first_or_404()
    url_data.clicks += 1
    db.session.commit()
    return redirect(url_data.original_url)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    url_data = URL.query.filter_by(short_code=short_code).first_or_404()
    return jsonify(url_data.to_dict())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
