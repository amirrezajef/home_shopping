from api.app_factory import db
from api.models import Option

def ensure_one_selected(option):
    """If marking one option as selected, unselect others of the same item"""
    if option.selected:
        Option.query.filter(Option.item_id==option.item_id, Option.id!=option.id).update({Option.selected: False})
        db.session.commit()