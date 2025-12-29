#!/usr/bin/env python3
"""
Database initialization script for Docker container
This script ensures the database is properly created with correct permissions
"""

import os
import sys

# Add the parent directory to the path so we can import from api package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app_factory import create_app
from api.app_factory import db
from api.models import Category, Subcategory

def init_database():
    """Initialize the database with proper setup"""
    app = create_app()
    with app.app_context():
        print("🗄️ Initializing database...")
        
        # Ensure instance directory exists and is writable
        instance_path = '/app/instance'
        if not os.path.exists(instance_path):
            os.makedirs(instance_path, mode=0o755)
            print(f"✅ Created instance directory: {instance_path}")
        
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if categories already exist
        if Category.query.first():
            print("✅ Categories already exist, skipping creation")
        else:
            print("🌱 Creating categories and subcategories...")
            
            # آشپزخانه
            kitchen = Category(name="آشپزخانه")
            db.session.add(kitchen)
            db.session.flush()
            
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
            print("✅ Categories and subcategories created successfully")
        
        print("🎉 Database initialization completed!")
        print("📊 Database file location: /app/instance/shopping.db")
        
        # Check file permissions
        db_file = os.path.join(instance_path, 'shopping.db')
        if os.path.exists(db_file):
            stat = os.stat(db_file)
            print(f"📁 Database file permissions: {oct(stat.st_mode)}")
            print(f"👤 Owner: {stat.st_uid}, Group: {stat.st_gid}")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
