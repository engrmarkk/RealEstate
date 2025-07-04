from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from sqlalchemy import Index
from .model_enum import TransactionType, TransactionStatus

# transactions


class Transaction(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    channel = db.Column(db.String(50))
    transaction_id = db.Column(db.String(50))
    transaction_type = db.Column(db.Enum(TransactionType), default=TransactionType.payment)
    transaction_status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.success)
    authorization_dict = db.Column(db.JSON)
    ip_address = db.Column(db.String(50))
    reference_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    property_purchased = db.relationship("PropertyPurchased", backref="transaction")
    __table_args__ = (
        Index("ix_transaction_created_at", "created_at"),
        Index("ix_transaction_updated_at", "updated_at"),
        Index("ix_transaction_user_id", "user_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M'),
            "amount": self.amount,
            "channel": self.channel,
            "transaction_type": self.transaction_type.value,
            "transaction_status": self.transaction_status.value,
            "reference_number": self.reference_number,
            "property_purchases": [
                {
                    "property_title": p.property.title if p.property else "N/A",
                    "amount": p.amount
                }
                for p in getattr(self, "property_purchased", [])
            ]
        }
