# URL Shortener

A modern URL shortening service built with Flask and SQLAlchemy.

## Features
- Create shortened URLs
- Track click statistics
- Modern, responsive design
- Copy to clipboard functionality
- Recent URLs display

## Installation

1. Clone the repository
```bash
git clone https://github.com/harryongit/url-shortener.git
cd url-shortener
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize database
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

5. Run the application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.
