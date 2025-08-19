from flask import Blueprint, jsonify, request
from api.app_factory import db
from api.models import Category, Subcategory

categories_bp = Blueprint('categories', __name__, url_prefix='/api')

@categories_bp.route('/init-db', methods=['POST'])
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

@categories_bp.route('/categories')
def get_categories():
    try:
        categories = Category.query.all()
        categories_data = []
        for category in categories:
            subcategories = [{'id': sub.id, 'name': sub.name} for sub in category.subcategories]
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'subcategories': subcategories
            })
        return jsonify({'categories': categories_data}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در دریافت دسته‌بندی‌ها: {str(e)}", "success": False}), 500

@categories_bp.route('/subcategories/<int:category_id>')
def get_subcategories(category_id):
    try:
        subcategories = Subcategory.query.filter_by(category_id=category_id).order_by(Subcategory.name).all()
        return jsonify({'subcategories': [{'id': sub.id, 'name': sub.name} for sub in subcategories]}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در دریافت زیردسته‌ها: {str(e)}", "success": False}), 500