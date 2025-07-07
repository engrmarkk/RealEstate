from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from models.model_enum import TourType, TourStatus, InquiryStatus


class Favorite(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (db.UniqueConstraint("user_id", "property_id"),)


class Inquiry(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default=InquiryStatus.pending)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    responded_at = db.Column(db.DateTime)


class Tour(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    tour_date = db.Column(db.Date)
    tour_time = db.Column(db.Time)
    tour_type = db.Column(db.String(20), default=TourType.in_person)
    status = db.Column(db.String(20), default=TourStatus.pending)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    confirmed_at = db.Column(db.DateTime)
