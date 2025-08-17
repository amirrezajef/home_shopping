#!/usr/bin/env python3
"""
Simple test script to check database state
"""

from app import app, db, Item, Category

def test_database():
    with app.app_context():
        print("🔍 Checking database state...")
        
        # Check categories
        categories = Category.query.all()
        print(f"📂 Found {len(categories)} categories:")
        for cat in categories:
            print(f"  - {cat.id}: {cat.name}")
        
        # Check items
        items = Item.query.all()
        print(f"\n📦 Found {len(items)} items:")
        for item in items:
            print(f"  - {item.id}: {item.name}")
            print(f"    Room: {item.room}")
            print(f"    Category ID: {item.category_id}")
            print(f"    Subcategory ID: {item.subcategory_id}")
            print()
        
        # Check items by room
        print("🏠 Items by room:")
        rooms = db.session.query(Item.room).distinct().all()
        for (room,) in rooms:
            if room:
                room_items = Item.query.filter_by(room=room).all()
                print(f"  {room}: {len(room_items)} items")
                for item in room_items:
                    print(f"    - {item.name}")

if __name__ == "__main__":
    test_database() 