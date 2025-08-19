from api.app_factory import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    room = db.Column(db.String(120))  # e.g., kitchen, bedroom, living room
    notes = db.Column(db.Text)
    budget = db.Column(db.Float)  # optional budget for the item
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    
    # Relationships
    options = relationship('Option', backref='item', cascade="all, delete")
    
    def __repr__(self):
        return f'<Item {self.name}>'