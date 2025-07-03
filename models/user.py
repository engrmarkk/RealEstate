from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as hasher
from sqlalchemy import Index


class Users(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    user_profile = db.relationship("UserProfile", backref="user", uselist=False)
    agent = db.relationship("Agent", backref="user", uselist=False)
    transactions = db.relationship("Transaction", backref="user")
    favorites = db.relationship("Favorite", backref="user")
    inquiries = db.relationship("Inquiry", backref="user")
    tours = db.relationship("Tour", backref="user")
    property_purchased = db.relationship("PropertyPurchased", backref="user")

    # indexes
    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_created_at", "created_at"),
        Index("ix_users_updated_at", "updated_at"),
        Index("ix_users_is_admin", "is_admin"),
    )

    def __init__(self, email, password, user_profile=None, agent=None):
        self.email = email.lower()
        self.password = hasher.hash(password)
        self.user_profile = user_profile
        self.agent = agent

    def check_password(self, password):
        return hasher.verify(password, self.password)


class UserProfile(db.Model):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(30))
    profile_image = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index("ix_user_profile_created_at", "created_at"),
        Index("ix_user_profile_updated_at", "updated_at"),
        Index("ix_user_profile_user_id", "user_id"),
        Index("ix_user_profile_first_name", "first_name"),
        Index("ix_user_profile_last_name", "last_name"),
    )
