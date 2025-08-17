from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopping.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# ---------- Routes ----------
@app.route('/init-db')
def init_db():
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
        flash("دیتابیس با موفقیت راه‌اندازی شد.", "success")
    else:
        flash("دیتابیس قبلاً راه‌اندازی شده است.", "info")
    return redirect(url_for('index'))

@app.route('/')
def index():
    # Get filter parameters
    category_filter = request.args.get('category', type=int)
    subcategory_filter = request.args.get('subcategory', type=int)
    
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
    if category_filter:
        items_query = items_query.filter(Item.category_id == category_filter)
    if subcategory_filter:
        items_query = items_query.filter(Item.subcategory_id == subcategory_filter)
    
    # Group items by category
    items_by_category = {}
    for category in categories:
        category_items = items_query.filter(Item.category_id == category.id).all()
        if category_items:
            items_by_category[category] = category_items
    
    recent_items = Item.query.order_by(Item.created_at.desc()).limit(10).all()
    
    return render_template('index.html',
                           total_items=total_items,
                           items_with_choice=items_with_choice,
                           completion=completion,
                           total_selected_cost=total_selected_cost,
                           total_budget=total_budget,
                           categories=categories,
                           items_by_category=items_by_category,
                           recent_items=recent_items,
                           current_category=category_filter,
                           current_subcategory=subcategory_filter)

@app.route('/items/new', methods=['GET', 'POST'])
def new_item():
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        name = request.form.get('name')
        room = request.form.get('room')
        notes = request.form.get('notes')
        budget = request.form.get('budget') or None
        category_id = request.form.get('category_id') or None
        subcategory_id = request.form.get('subcategory_id') or None
        
        if not name:
            flash("نام وسیله الزامی است.", "danger")
            return render_template('new_item.html', categories=categories)

        item = Item(name=name, room=room, notes=notes,
                    budget=float(budget) if budget else None,
                    category_id=int(category_id) if category_id else None,
                    subcategory_id=int(subcategory_id) if subcategory_id else None)
        db.session.add(item)
        db.session.commit()
        flash("وسیله اضافه شد.", "success")
        return redirect(url_for('item_detail', item_id=item.id))
    return render_template('new_item.html', categories=categories)

@app.route('/items/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    options = Option.query.filter_by(item_id=item_id).order_by(Option.price.asc().nullslast()).all()
    # Prepare chart data
    labels = [o.label() for o in options]
    prices = [o.price or 0 for o in options]
    ratings = [o.rating or 0 for o in options]
    return render_template('item_detail.html', item=item, options=options, labels=labels, prices=prices, ratings=ratings)

@app.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash("وسیله حذف شد.", "info")
    return redirect(url_for('index'))

@app.route('/options/new/<int:item_id>', methods=['POST'])
def add_option(item_id):
    item = Item.query.get_or_404(item_id)
    o = Option(
        item_id=item_id,
        brand=request.form.get('brand'),
        model_name=request.form.get('model_name'),
        price=float(request.form.get('price')) if request.form.get('price') else None,
        store=request.form.get('store'),
        link=request.form.get('link'),
        features=request.form.get('features'),
        rating=float(request.form.get('rating')) if request.form.get('rating') else None,
        warranty_months=int(request.form.get('warranty_months')) if request.form.get('warranty_months') else None,
        available=True if request.form.get('available') == 'on' else False,
        notes=request.form.get('notes'),
        last_checked=datetime.utcnow().date()
    )
    db.session.add(o)
    db.session.commit()
    flash("مدل/گزینه اضافه شد.", "success")
    return redirect(url_for('item_detail', item_id=item_id))

@app.route('/options/<int:option_id>/select', methods=['POST'])
def select_option(option_id):
    option = Option.query.get_or_404(option_id)
    option.selected = True
    db.session.commit()
    ensure_one_selected(option)
    flash("این گزینه به عنوان انتخاب نهایی علامت خورد.", "success")
    return redirect(url_for('item_detail', item_id=option.item_id))

@app.route('/options/<int:option_id>/unselect', methods=['POST'])
def unselect_option(option_id):
    option = Option.query.get_or_404(option_id)
    option.selected = False
    db.session.commit()
    flash("گزینه از حالت انتخاب خارج شد.", "info")
    return redirect(url_for('item_detail', item_id=option.item_id))

@app.route('/options/<int:option_id>/delete', methods=['POST'])
def delete_option(option_id):
    option = Option.query.get_or_404(option_id)
    item_id = option.item_id
    db.session.delete(option)
    db.session.commit()
    flash("گزینه حذف شد.", "info")
    return redirect(url_for('item_detail', item_id=item_id))

# Simple CSV export for selected options
@app.route('/export/selected.csv')
def export_selected():
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

@app.route('/api/subcategories/<int:category_id>')
def get_subcategories(category_id):
    subcategories = Subcategory.query.filter_by(category_id=category_id).order_by(Subcategory.name).all()
    return {'subcategories': [{'id': sub.id, 'name': sub.name} for sub in subcategories]}

if __name__ == '__main__':
    # Get host and port from environment variables or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host=host, port=port, debug=False)
