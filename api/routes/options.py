from flask import Blueprint, jsonify, request
from datetime import datetime
from api.app_factory import db
from api.models import Option, Item
from api.utils.helpers import ensure_one_selected

options_bp = Blueprint('options', __name__, url_prefix='/api')

@options_bp.route('/options', methods=['POST'])
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

@options_bp.route('/options/<int:option_id>/select', methods=['PUT'])
def select_option(option_id):
    try:
        option = Option.query.get_or_404(option_id)
        option.selected = True
        db.session.commit()
        ensure_one_selected(option)
        return jsonify({"message": "این گزینه به عنوان انتخاب نهایی علامت خورد.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در انتخاب گزینه: {str(e)}", "success": False}), 500

@options_bp.route('/options/<int:option_id>/unselect', methods=['PUT'])
def unselect_option(option_id):
    try:
        option = Option.query.get_or_404(option_id)
        option.selected = False
        db.session.commit()
        return jsonify({"message": "گزینه از حالت انتخاب خارج شد.", "success": True}), 200
    except Exception as e:
        return jsonify({"message": f"خطا در خارج کردن گزینه از حالت انتخاب: {str(e)}", "success": False}), 500

@options_bp.route('/options/<int:option_id>', methods=['PUT', 'DELETE'])
def option_detail(option_id):
    option = Option.query.get_or_404(option_id)
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            if 'brand' in data:
                option.brand = data['brand']
            if 'model_name' in data:
                option.model_name = data['model_name']
            if 'price' in data:
                option.price = float(data['price']) if data['price'] else None
            if 'store' in data:
                option.store = data['store']
            if 'link' in data:
                option.link = data['link']
            if 'features' in data:
                option.features = data['features']
            if 'rating' in data:
                option.rating = float(data['rating']) if data['rating'] else None
            if 'warranty_months' in data:
                option.warranty_months = int(data['warranty_months']) if data['warranty_months'] else None
            if 'available' in data:
                option.available = data['available']
            if 'notes' in data:
                option.notes = data['notes']
            
            db.session.commit()
            return jsonify({"message": "گزینه با موفقیت به‌روزرسانی شد.", "success": True}), 200
        except Exception as e:
            return jsonify({"message": f"خطا در به‌روزرسانی گزینه: {str(e)}", "success": False}), 500
    
    elif request.method == 'DELETE':
        try:
            item_id = option.item_id
            db.session.delete(option)
            db.session.commit()
            return jsonify({"message": "گزینه حذف شد.", "success": True}), 200
        except Exception as e:
            return jsonify({"message": f"خطا در حذف گزینه: {str(e)}", "success": False}), 500