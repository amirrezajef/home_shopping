from flask import Blueprint, jsonify, request
from api.app_factory import db
from api.models import Item, Option, Category, Subcategory

items_bp = Blueprint('items', __name__, url_prefix='/api')

@items_bp.route('/items', methods=['GET', 'POST'])
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

@items_bp.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
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