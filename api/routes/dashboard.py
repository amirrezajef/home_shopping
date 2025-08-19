from flask import Blueprint, jsonify, request
from sqlalchemy import func
from api.app_factory import db
from api.models import Category, Subcategory, Item, Option

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api')

@dashboard_bp.route('/dashboard')
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