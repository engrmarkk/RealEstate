from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime

# transactions


class Transaction(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    reference_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
