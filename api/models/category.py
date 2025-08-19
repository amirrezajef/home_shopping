from api.app_factory import db
from sqlalchemy.orm import relationship

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    
    # Relationships
    subcategories = relationship('Subcategory', backref='category', lazy=True, cascade="all, delete-orphan")
    items = relationship('Item', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'