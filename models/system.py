from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from sqlalchemy import Index


class Newsletter(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.now)
    unsubscribed_at = db.Column(db.DateTime)

    __table_args__ = (
        Index("ix_newsletter_subscribed_at", "subscribed_at"),
        Index("ix_newsletter_unsubscribed_at", "unsubscribed_at"),
        Index("ix_newsletter_email", "email", unique=True),
        Index("ix_newsletter_is_active", "is_active"),
    )


class Contact(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text)
    opened = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index("ix_contact_created_at", "created_at"),
        Index("ix_contact_updated_at", "updated_at"),
    )


class PropertyView(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index("ix_property_view_created_at", "created_at"),
        Index("ix_property_view_updated_at", "updated_at"),
        Index("ix_property_view_property_id", "property_id"),
    )
