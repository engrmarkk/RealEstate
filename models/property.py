from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from sqlalchemy import Index
from models.model_enum import PropertyType, PropertyStatus, ListingType


class Property(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    title = db.Column(db.String(50))
    description = db.Column(db.String(255))
    property_type = db.Column(db.Enum(PropertyType), default=PropertyType.apartment)
    listing_type = db.Column(db.Enum(ListingType), default=ListingType.for_sale)
    property_status = db.Column(
        db.Enum(PropertyStatus), nullable=False, default=PropertyStatus.active
    )
    price = db.Column(db.Float)
    address = db.Column(db.String(255))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    land_details = db.relationship("LandDetails", backref="property", uselist=False)
    house_details = db.relationship("HouseDetails", backref="property", uselist=False)
    property_images = db.relationship("PropertyImages", backref="property")
    property_views = db.relationship("PropertyView", backref="property")
    transactions = db.relationship("Transaction", backref="property")
    favorites = db.relationship("Favorite", backref="property")
    inquiries = db.relationship("Inquiry", backref="property")
    tours = db.relationship("Tour", backref="property")
    property_purchased = db.relationship("PropertyPurchased", backref="property")

    __table_args__ = (
        Index("ix_property_created_at", "created_at"),
        Index("ix_property_updated_at", "updated_at"),
        Index("ix_property_property_type", "property_type"),
        Index("ix_property_listing_type", "listing_type"),
        Index("ix_property_property_status", "property_status"),
        Index("ix_property_price", "price"),
        Index("ix_property_address", "address"),
        Index("ix_property_state", "state"),
        Index("ix_property_city", "city"),
    )


# land details
class LandDetails(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    area_sqft = db.Column(db.Integer)
    size = db.Column(db.Float)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# house details
class HouseDetails(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Integer, default=0)
    garage_spaces = db.Column(db.Integer, default=0)
    has_pool = db.Column(db.Boolean, default=False)
    has_garden = db.Column(db.Boolean, default=False)
    has_balcony = db.Column(db.Boolean, default=False)
    has_elevator = db.Column(db.Boolean, default=False)
    is_furnished = db.Column(db.Boolean, default=False)
    is_pet_friendly = db.Column(db.Boolean, default=False)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# property images
class PropertyImages(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    image_url = db.Column(db.String(255))
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# property purchased
class PropertyPurchased(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.UniqueConstraint("property_id", "user_id"),
        Index("ix_property_purchased_created_at", "created_at"),
        Index("ix_property_purchased_updated_at", "updated_at"),
        Index("ix_property_purchased_property_id", "property_id"),
        Index("ix_property_purchased_user_id", "user_id"),
    )
