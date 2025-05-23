from flask import Flask
import os
import logging
from dotenv import load_dotenv
from config.database import connect_db 

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
app = Flask(__name__)

def create_app():
    """Application factory function"""
    app = Flask(__name__)

    # Connect to MongoDB
    mongo_client = connect_db()
    app.db = mongo_client.get_database()  # Optional: bisa ganti dengan nama DB spesifik
    app.db = mongo_client["test"]

    # Register routes
    from routes.audio_routes import audio_bp
    from routes.health_routes import health_bp
    from routes.index_routes import index_bp

    app.register_blueprint(index_bp, url_prefix='')
    app.register_blueprint(audio_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('ENVIRONMENT', 'production').lower() == 'development'

    logger.info(f"Starting server on port {port}, debug mode: {debug}")
    app.run(host='0.0.0.0', port=port, debug=debug)
