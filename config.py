import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cro-ontology-sentiment-system-secret-2026'
    
    # Database configuration
    INSTANCE_DIR = os.path.join(basedir, 'instance')
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(INSTANCE_DIR, 'sentiment_analysis.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Knowledge base & sample files
    ONTOLOGY_PATH = os.path.join(basedir, 'ontology', 'customer_review_ontology.owl')
    SAMPLE_DATA_PATH = os.path.join(basedir, 'sample_data', 'sample_reviews.csv')
    REPORTS_DIR = os.path.join(basedir, 'reports')
    os.makedirs(REPORTS_DIR, exist_ok=True)

class TestingConfig(Config):
    """Configuration for automated test execution."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
