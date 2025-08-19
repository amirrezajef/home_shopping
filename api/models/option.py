from api.app_factory import db
from datetime import date

class Option(db.Model):
    __tablename__ = 'option'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    brand = db.Column(db.String(120))
    model_name = db.Column(db.String(200))
    price = db.Column(db.Float)
    store = db.Column(db.String(200))
    link = db.Column(db.String(400))
    features = db.Column(db.Text)  # comma-separated or free text
    rating = db.Column(db.Float)  # 0-10 user score
    warranty_months = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    selected = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.Date)
    
    def label(self):
        parts = [self.brand or '', self.model_name or '']
        return " ".join([p for p in parts if p]).strip() or f"Option #{self.id}"
    
    def __repr__(self):
        return f'<Option {self.model_name}>'