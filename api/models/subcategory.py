from api.app_factory import db
from sqlalchemy.orm import relationship

class Subcategory(db.Model):
    __tablename__ = 'subcategory'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Relationships
    items = relationship('Item', backref='subcategory', lazy=True)
    
    def __repr__(self):
        return f'<Subcategory {self.name}>'