from flask import Flask
from flask_cors import CORS
from app.config.settings import Config
from app.routes.url_routes import url_blueprint
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(url_blueprint, url_prefix='/api/v1')
    
    # Basic health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'version': os.getenv('APP_VERSION', '1.0.0')}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', False))