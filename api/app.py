from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for React frontend
CORS(app)

db = SQLAlchemy(app)

# ---------- Models ----------
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True, cascade="all, delete-orphan")
    items = db.relationship('Item', backref='category', lazy=True)

class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    items = db.relationship('Item', backref='subcategory', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    room = db.Column(db.String(120))  # e.g., kitchen, bedroom, living room
    notes = db.Column(db.Text)
    budget = db.Column(db.Float)  # optional budget for the item
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    options = db.relationship('Option', backref='item', cascade="all, delete")

class Option(db.Model):
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

# ---------- Helpers ----------
def ensure_one_selected(option):
    # If marking one option as selected, unselect others of the same item
    if option.selected:
        Option.query.filter(Option.item_id==option.item_id, Option.id!=option.id).update({Option.selected: False})
        db.session.commit()

# ---------- API Routes ----------
@app.route('/api/init-db', methods=['POST'])
def init_db():
    try:
        db.create_all()
        # Seed categories and subcategories
        if not Category.query.first():
            # آشپزخانه
            kitchen = Category(name="آشپزخانه")
            db.session.add(kitchen)
            db.session.flush()  # Get the ID
            
            kitchen_subs = [
                "یخچال و فریزر", "اجاق گاز", "فر برقی", "مایکروویو", "هود آشپزخانه",
                "ماشین ظرفشویی", "سینک ظرفشویی", "کابینت و قفسه", "ظروف پخت‌وپز",
                "سرویس بشقاب", "سرویس چاقو", "مخلوط‌کن و غذاساز", "آبمیوه‌گیری",
                "چای‌ساز", "ماشین قهوه‌ساز", "ابزار آشپزی", "تخته برش",
                "ظرف نگهداری غذا", "کیسه فریزر"
            ]
            for sub_name in kitchen_subs:
                db.session.add(Subcategory(name=sub_name, category_id=kitchen.id))
            
            # اتاق خواب
            bedroom = Category(name="اتاق خواب")
            db.session.add(bedroom)
            db.session.flush()
            
            bedroom_subs = [
                "تخت‌خواب و تشک", "ملحفه و روبالشی", "کمد لباس", "میز آرایش",
                "آینه", "پرده و فرش", "چراغ خواب", "جعبه جواهرات"
            ]
            for sub_name in bedroom_subs:
                db.session.add(Subcategory(name=sub_name, category_id=bedroom.id))
            
            # نشیمن
            living = Category(name="نشیمن")
            db.session.add(living)
            db.session.flush()
            
            living_subs = [
                "مبلمان", "تلویزیون و میز", "سیستم صوتی", "فرش و قالیچه",
                "پرده", "کتابخانه", "لامپ و لوستر", "تابلو و تزئینات"
            ]
            for sub_name in living_subs:
                db.session.add(Subcategory(name=sub_name, category_id=living.id))
            
            # حمام و سرویس
            bathroom = Category(name="حمام و سرویس")
            db.session.add(bathroom)
            db.session.flush()
            
            bathroom_subs = [
                "ماشین لباسشویی", "خشک‌کن لباس", "روشویی و آینه", "وان یا دوش",
                "جا حوله‌ای", "مواد شوینده", "جا مسواکی", "کفپوش ضدلغزش"
            ]
            for sub_name in bathroom_subs:
                db.session.add(Subcategory(name=sub_name, category_id=bathroom.id))
            
            # نظافت
            cleaning = Category(name="نظافت")
            db.session.add(cleaning)
            db.session.flush()
            
            cleaning_subs = [
                "جاروبرقی", "جارو دستی", "تی و سطل", "دستمال نظافت",
                "مواد شوینده", "سطل زباله"
            ]
            for sub_name in cleaning_subs:
                db.session.add(Subcategory(name=sub_name, category_id=cleaning.id))
            
            # ایمنی
            safety = Category(name="ایمنی")
            db.session.add(safety)
            db.session.flush()
            
            safety_subs = [
                "جعبه کمک‌های اولیه", "کپسول آتش‌نشانی", "قفل ایمن",
                "چراغ‌قوه", "باتری و چندراهی"
            ]
            for sub_name in safety_subs:
                db.session.add(Subcategory(name=sub_name, category_id=safety.id))
            
            # عمومی
            general = Category(name="عمومی")
            db.session.add(general)
            db.session.flush()
            
            general_subs = [
                "میز ناهارخوری", "گلدان و گیاهان", "ساعت دیواری",
                "پله‌بان", "ابزارآلات", "چرخ خرید"
            ]
            for sub_name in general_subs:
                db.session.add(Subcategory(name=sub_name, category_id=general.id))
            
            db.session.commit()
            return jsonify({"message": "دیتابیس با موفقیت راه‌اندازی شد.", "success": True}), 200
        else:
            return jsonify({"message": "دیتابیس قبلاً راه‌اندازی شده است.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در راه‌اندازی دیتابیس: {str(e)}", "success": False}), 500

@app.route('/api/dashboard')
def dashboard():
    try:
        # Get filter parameters - frontend sends category names as strings
        category_filter = request.args.get('category', '')
        subcategory_filter = request.args.get('subcategory', '')
        
        # Dashboard stats
        total_items = Item.query.count()
        items_with_choice = Item.query.join(Option).filter(Option.selected==True).distinct().count()
        completion = int((items_with_choice / total_items) * 100) if total_items else 0

        # Cost summaries
        total_selected_cost = db.session.query(func.sum(Option.price)).filter(Option.selected==True).scalar() or 0
        total_budget = db.session.query(func.sum(Item.budget)).scalar() or 0

        # List items grouped by category with filtering
        categories = Category.query.order_by(Category.name).all()
        
        # Apply filters
        items_query = Item.query
        if category_filter and category_filter != 'all':
            category_obj = Category.query.filter(Category.name == category_filter).first()
            if category_obj:
                items_query = items_query.filter(Item.category_id == category_obj.id)
        if subcategory_filter and subcategory_filter != 'all':
            subcategory_obj = Subcategory.query.filter(Subcategory.name == subcategory_filter).first()
            if subcategory_obj:
                items_query = items_query.filter(Item.subcategory_id == subcategory_obj.id)
        
        # Get all items for display (not just by category)
        all_items = items_query.all()
        items_data = [
            {
                'id': item.id,
                'name': item.name,
                'room': item.room,
                'notes': item.notes,
                'budget': item.budget,
                'created_at': item.created_at.isoformat() if item.created_at else None,
                'category_id': item.category_id,
                'subcategory_id': item.subcategory_id,
                'options_count': len(item.options),
                'selected_option': next(({
                    'id': opt.id,
                    'brand': opt.brand,
                    'model_name': opt.model_name,
                    'price': opt.price,
                    'store': opt.store,
                    'link': opt.link,
                    'features': opt.features,
                    'rating': opt.rating,
                    'warranty_months': opt.warranty_months,
                    'available': opt.available,
                    'notes': opt.notes,
                    'selected': opt.selected,
                    'last_checked': opt.last_checked.isoformat() if opt.last_checked else None
                } for opt in item.options if opt.selected), None),
                'category': item.category.name if item.category else None,
                'subcategory': item.subcategory.name if item.subcategory else None
            }
            for item in all_items
        ]
        
        # Group items by category for the items_by_category structure
        items_by_category = {}
        for category in categories:
            # Get items by category_id first
            category_items = items_query.filter(Item.category_id == category.id).all()
            
            # Also get items by room name if it matches the category name
            room_items = items_query.filter(Item.room == category.name).all()
            
            # Combine both sets of items, avoiding duplicates
            all_category_items = list(set(category_items + room_items))
            
            if all_category_items:
                items_by_category[category.name] = [
                    {
                        'id': item.id,
                        'name': item.name,
                        'room': item.room,
                        'notes': item.notes,
                        'budget': item.budget,
                        'created_at': item.created_at.isoformat() if item.created_at else None,
                        'category_id': item.category_id,
                        'subcategory_id': item.subcategory_id,
                        'options_count': len(item.options),
                        'selected_option': next(({
                            'id': opt.id,
                            'brand': opt.brand,
                            'model_name': opt.model_name,
                            'price': opt.price,
                            'store': opt.store,
                            'link': opt.link,
                            'features': opt.features,
                            'rating': opt.rating,
                            'warranty_months': opt.warranty_months,
                            'available': opt.available,
                            'notes': opt.notes,
                            'selected': opt.selected,
                            'last_checked': opt.last_checked.isoformat() if opt.last_checked else None
                        } for opt in item.options if opt.selected), None)
                    }
                    for item in all_category_items
                ]
        
        # Add items that don't have a category but have a room to a "سایر" category
        uncategorized_items = items_query.filter(
            Item.category_id.is_(None),
            Item.room.isnot(None)
        ).all()
        
        if uncategorized_items:
            items_by_category["سایر"] = [
                {
                    'id': item.id,
                    'name': item.name,
                    'room': item.room,
                    'notes': item.notes,
                    'budget': item.budget,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'category_id': item.category_id,
                    'subcategory_id': item.subcategory_id,
                    'options_count': len(item.options),
                                            'selected_option': next(({
                            'id': opt.id,
                            'brand': opt.brand,
                            'model_name': opt.model_name,
                            'price': opt.price,
                            'store': opt.store,
                            'link': opt.link,
                            'features': opt.features,
                            'rating': opt.rating,
                            'warranty_months': opt.warranty_months,
                            'available': opt.available,
                            'notes': opt.notes,
                            'selected': opt.selected,
                            'last_checked': opt.last_checked.isoformat() if opt.last_checked else None
                        } for opt in item.options if opt.selected), None)
                }
                for item in uncategorized_items
            ]
        
        # Build subcategories structure
        subcategories = {}
        for category in categories:
            subcategories[category.name] = [sub.name for sub in category.subcategories]
        
        recent_items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
        recent_items_data = [
            {
                'id': item.id,
                'name': item.name,
                'room': item.room,
                'created_at': item.created_at.isoformat() if item.created_at else None
            }
            for item in recent_items
        ]
        
        return jsonify({
            'total_items': total_items,
            'items_with_choice': items_with_choice,
            'completion': completion,
            'total_selected_cost': total_selected_cost,
            'total_budget': total_budget,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in categories],
            'subcategories': subcategories,
            'items': items_data,
            'items_by_category': items_by_category,
            'recent_items': recent_items_data,
            'current_category': category_filter,
            'current_subcategory': subcategory_filter
        }), 200
    except Exception as e:
        return jsonify({"message": f"خطا در دریافت اطلاعات: {str(e)}", "success": False}), 500

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        try:
            items = Item.query.all()
            items_data = [
                {
                    'id': item.id,
                    'name': item.name,
                    'room': item.room,
                    'notes': item.notes,
                    'budget': item.budget,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'category_id': item.category_id,
                    'subcategory_id': item.subcategory_id,
                    'options_count': len(item.options)
                }
                for item in items
            ]
            return jsonify(items_data), 200
        except Exception as e:
            return jsonify({"message": f"خطا در دریافت آیتم‌ها: {str(e)}", "success": False}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name')
            room = data.get('room')
            notes = data.get('notes')
            budget = data.get('budget')
            category_id = data.get('category_id')
            subcategory_id = data.get('subcategory_id')
            
            if not name:
                return jsonify({"message": "نام وسیله الزامی است.", "success": False}), 400

            item = Item(
                name=name, 
                room=room, 
                notes=notes,
                budget=float(budget) if budget else None,
                category_id=int(category_id) if category_id else None,
                subcategory_id=int(subcategory_id) if subcategory_id else None
            )
            db.session.add(item)
            db.session.commit()
            
            return jsonify({
                "message": "وسیله اضافه شد.",
                "success": True,
                "item": {
                    'id': item.id,
                    'name': item.name,
                    'room': item.room,
                    'notes': item.notes,
                    'budget': item.budget,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'category_id': item.category_id,
                    'subcategory_id': item.subcategory_id
                }
            }), 201
        except Exception as e:
            return jsonify({"message": f"خطا در اضافه کردن آیتم: {str(e)}", "success": False}), 500

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'GET':
        try:
            options = Option.query.filter_by(item_id=item_id).order_by(Option.price.asc().nullslast()).all()
            options_data = [
                {
                    'id': opt.id,
                    'brand': opt.brand,
                    'model_name': opt.model_name,
                    'price': opt.price,
                    'store': opt.store,
                    'link': opt.link,
                    'features': opt.features,
                    'rating': opt.rating,
                    'warranty_months': opt.warranty_months,
                    'available': opt.available,
                    'notes': opt.notes,
                    'selected': opt.selected,
                    'last_checked': opt.last_checked.isoformat() if opt.last_checked else None
                }
                for opt in options
            ]
            
            # Determine item status based on whether any option is selected
            item_status = 'selected' if any(opt['selected'] for opt in options_data) else 'not_selected'
            
            return jsonify({
                'item': {
                    'id': item.id,
                    'name': item.name,
                    'room': item.room,
                    'notes': item.notes,
                    'budget': item.budget,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'category_id': item.category_id,
                    'subcategory_id': item.subcategory_id,
                    'category': item.category.name if item.category else None,
                    'subcategory': item.subcategory.name if item.subcategory else None,
                    'status': item_status
                },
                'options': options_data
            }), 200
        except Exception as e:
            return jsonify({"message": f"خطا در دریافت اطلاعات: {str(e)}", "success": False}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            if 'name' in data:
                item.name = data['name']
            if 'room' in data:
                item.room = data['room']
            if 'notes' in data:
                item.notes = data['notes']
            if 'budget' in data:
                item.budget = float(data['budget']) if data['budget'] else None
            if 'category_id' in data:
                item.category_id = int(data['category_id']) if data['category_id'] else None
            if 'subcategory_id' in data:
                item.subcategory_id = int(data['subcategory_id']) if data['subcategory_id'] else None
            
            db.session.commit()
            return jsonify({"message": "آیتم با موفقیت به‌روزرسانی شد.", "success": True}), 200
        except Exception as e:
            return jsonify({"message": f"خطا در به‌روزرسانی آیتم: {str(e)}", "success": False}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "وسیله حذف شد.", "success": True}), 200
        except Exception as e:
            return jsonify({"message": f"خطا در حذف آیتم: {str(e)}", "success": False}), 500

@app.route('/api/options', methods=['POST'])
def add_option():
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        
        if not item_id:
            return jsonify({"message": "شناسه آیتم الزامی است.", "success": False}), 400
        
        item = Item.query.get_or_404(item_id)
        
        option = Option(
            item_id=item_id,
            brand=data.get('brand'),
            model_name=data.get('model_name'),
            price=float(data.get('price')) if data.get('price') else None,
            store=data.get('store'),
            link=data.get('link'),
            features=data.get('features'),
            rating=float(data.get('rating')) if data.get('rating') else None,
            warranty_months=int(data.get('warranty_months')) if data.get('warranty_months') else None,
            available=data.get('available', True),
            notes=data.get('notes'),
            last_checked=datetime.utcnow().date()
        )
        
        db.session.add(option)
        db.session.commit()
        
        return jsonify({
            "message": "مدل/گزینه اضافه شد.",
            "success": True,
            "option": {
                'id': option.id,
                'brand': option.brand,
                'model_name': option.model_name,
                'price': option.price,
                'store': option.store,
                'link': option.link,
                'features': option.features,
                'rating': option.rating,
                'warranty_months': option.warranty_months,
                'available': option.available,
                'notes': option.notes,
                'selected': option.selected,
                'last_checked': option.last_checked.isoformat() if option.last_checked else None
            }
        }), 201
    except Exception as e:
        return jsonify({"message": f"خطا در اضافه کردن گزینه: {str(e)}", "success": False}), 500

@app.route('/api/options/<int:option_id>/select', methods=['PUT'])
def select_option(option_id):
    try:
        option = Option.query.get_or_404(option_id)
        option.selected = True
        db.session.commit()
        ensure_one_selected(option)
        return jsonify({"message": "این گزینه به عنوان انتخاب نهایی علامت خورد.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در انتخاب گزینه: {str(e)}", "success": False}), 500

@app.route('/api/options/<int:option_id>/unselect', methods=['PUT'])
def unselect_option(option_id):
    try:
        option = Option.query.get_or_404(option_id)
        option.selected = False
        db.session.commit()
        return jsonify({"message": "گزینه از حالت انتخاب خارج شد.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در خارج کردن گزینه از حالت انتخاب: {str(e)}", "success": False}), 500

@app.route('/api/options/<int:option_id>', methods=['DELETE'])
def delete_option(option_id):
    try:
        option = Option.query.get_or_404(option_id)
        item_id = option.item_id
        db.session.delete(option)
        db.session.commit()
        return jsonify({"message": "گزینه حذف شد.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در حذف گزینه: {str(e)}", "success": False}), 500

@app.route('/api/export/selected.csv')
def export_selected():
    try:
        from flask import Response
        rows = Option.query.filter_by(selected=True).all()
        def gen():
            yield "Item,Brand,Model,Price,Store,Link,Rating,Notes\n"
            for r in rows:
                def s(x):
                    return (str(x or "")).replace('"', '""')
                line = f'"{s(r.item.name)}","{s(r.brand)}","{s(r.model_name)}","{s(r.price)}","{s(r.store)}","{s(r.link)}","{s(r.rating)}","{s(r.notes)}"\n'
                yield line
        return Response(gen(), mimetype='text/csv',
                        headers={"Content-Disposition": "attachment;filename=selected_options.csv"})
    except Exception as e:
        return jsonify({"message": f"خطا در صادرات: {str(e)}", "success": False}), 500

@app.route('/api/subcategories/<int:category_id>')
def get_subcategories(category_id):
    try:
        subcategories = Subcategory.query.filter_by(category_id=category_id).order_by(Subcategory.name).all()
        return jsonify({'subcategories': [{'id': sub.id, 'name': sub.name} for sub in subcategories]}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در دریافت زیردسته‌ها: {str(e)}", "success": False}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for Docker"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "home-shopping-api"
    }), 200

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host=host, port=port, debug=False) 