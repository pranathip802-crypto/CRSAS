import os
from flask import Flask, render_template
from config import Config
from models import db, User, Product
from services.ontology_service import OntologyService
from services.sentiment_analyzer import SentimentAnalyzer

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Initialize Ontology and Sentiment Analyzer services
    ontology_path = app.config['ONTOLOGY_PATH']
    ontology_service = OntologyService(ontology_path)
    sentiment_analyzer = SentimentAnalyzer(ontology_service)
    
    app.ontology_service = ontology_service
    app.sentiment_analyzer = sentiment_analyzer

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.review_routes import review_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.ontology_routes import ontology_bp
    from routes.report_routes import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ontology_bp)
    app.register_blueprint(report_bp)

    # Home / Landing page route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # First-time database setup and seed
    with app.app_context():
        db.create_all()
        _seed_initial_data()

    return app

def _seed_initial_data():
    """Seeds default administrator and catalog products safely if not already present."""
    # 1. Seed Admin
    admin_email = "admin@sentiment.local"
    if not User.query.filter_by(email=admin_email).first():
        admin = User(name="Administrator", email=admin_email, role="admin")
        admin.set_password("Admin@12345")
        db.session.add(admin)

    # 2. Seed Standard Products
    sample_products = [
        ("iPhone 15 Pro", "Smartphone", "Apple flagship smartphone with A17 Pro chip and titanium design."),
        ("Samsung Galaxy S24", "Smartphone", "Flagship Android device with Dynamic AMOLED display and AI camera."),
        ("Google Pixel 8", "Smartphone", "Google smartphone featuring computational photography and Tensor G3."),
        ("MacBook Pro M3", "Laptop", "Apple premium laptop featuring M3 silicon and Liquid Retina XDR display."),
        ("Dell XPS 15", "Laptop", "High-performance Windows laptop with OLED infinity display."),
        ("Lenovo ThinkPad X1", "Laptop", "Business-grade laptop renowned for keyboard comfort and durability."),
        ("Sony WH-1000XM5", "Headphones", "Industry-leading active noise cancelling wireless headphones."),
        ("Bose QuietComfort 45", "Headphones", "Ergonomic headphones featuring acoustic noise cancelling."),
        ("AirPods Pro 2", "Headphones", "Wireless earbuds with adaptive audio and spatial transparency."),
        ("Amazon Shopping", "OnlineShopping", "Global retail e-commerce platform offering doorstep delivery."),
        ("Flipkart Order", "OnlineShopping", "Leading online marketplace offering consumer electronics and apparel.")
    ]

    for p_name, p_cat, p_desc in sample_products:
        if not Product.query.filter_by(name=p_name).first():
            db.session.add(Product(name=p_name, category=p_cat, description=p_desc))

    db.session.commit()

app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print(" Ontology-Based Customer Review Sentiment Analysis System")
    print(" Running on: http://127.0.0.1:5000")
    print(" Default Admin: admin@sentiment.local | Password: Admin@12345")
    print("=" * 70)
    app.run(debug=True, host='127.0.0.1', port=5000)
