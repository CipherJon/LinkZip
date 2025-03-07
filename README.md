# LinkZip - URL Shortener Application

## Features
- Shorten long URLs to compact codes
- Redirect short URLs to original destinations
- REST API endpoints for integration
- SQLAlchemy database integration
- Unit and integration testing
- Custom short code generation

## Installation
```bash
# Clone repository
git clone https://github.com/yourusername/LinkZip.git
cd LinkZip

# Install dependencies
pip install -r requirements.txt
```

## Configuration
1. Create `.env` file:
```ini
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
```

2. Initialize database:
```bash
flask db upgrade
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/shorten` | POST | Create short URL (requires JSON: `{"url": "https://..."}`) |
| `/api/<short_code>` | GET | Get original URL details |
| `/<short_code>` | GET | Redirect to original URL |

## Database Structure
```python
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048))
    short_code = db.Column(db.String(16), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## Running the Application
```bash
flask run --host=0.0.0.0 --port=5000
```

## Testing
```bash
# Run all tests
python -m pytest tests/
```

## Contributing
1. Fork the repository
2. Create feature branch
3. Submit pull request with tests
