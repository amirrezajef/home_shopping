from flask import Blueprint, Response, jsonify
from api.models import Option

export_bp = Blueprint('export', __name__, url_prefix='/api')

@export_bp.route('/export/selected.csv')
def export_selected():
    try:
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