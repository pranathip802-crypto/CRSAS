from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    reviews = db.relationship('Review', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    
    reviews = db.relationship('Review', backref='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name} ({self.category})>'


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True, index=True)
    
    original_text = db.Column(db.Text, nullable=False)
    cleaned_text = db.Column(db.Text, nullable=False)
    overall_sentiment = db.Column(db.String(30), nullable=False, index=True)  # Positive, Negative, Neutral, Mixed
    sentiment_score = db.Column(db.Float, default=0.0)
    analysis_explanation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    feature_sentiments = db.relationship('FeatureSentiment', backref='review', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Review {self.id}: {self.overall_sentiment} ({self.sentiment_score:.2f})>'


class FeatureSentiment(db.Model):
    __tablename__ = 'feature_sentiments'
    
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False, index=True)
    feature_name = db.Column(db.String(100), nullable=False, index=True)
    opinion_words = db.Column(db.String(255), nullable=True)
    sentiment = db.Column(db.String(30), nullable=False, index=True)  # Positive, Negative, Neutral, Mixed
    score = db.Column(db.Float, default=0.0)
    ontology_evidence = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<FeatureSentiment {self.feature_name}: {self.sentiment}>'
