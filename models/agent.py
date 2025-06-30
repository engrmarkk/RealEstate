from flask_login import UserMixin
from extensions import db
from utils.util import generate_db_id
from datetime import datetime
from models.model_enum import CommissionRecordType
from sqlalchemy import Index


# agent
class Agent(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    agent_code = db.Column(db.String(50), unique=True)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    specialization = db.Column(db.String(100))
    bio = db.Column(db.Text)
    office_address = db.Column(db.String(255))
    office_phone = db.Column(db.String(20))
    commission_rate = db.Column(db.Float, default=0.0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    agent_wallet = db.relationship(
        "AgentWallet", backref="agent", cascade="all, delete-orphan"
    )
    commission_record = db.relationship(
        "CommissionRecord", backref="agent", cascade="all, delete-orphan"
    )
    agent_bank_details = db.relationship(
        "AgentBankDetails", backref="agent", cascade="all, delete-orphan"
    )
    commission_rate_change = db.relationship(
        "CommissionRateChange", backref="agent", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_agent_created_at", "created_at"),
        Index("ix_agent_updated_at", "updated_at"),
        Index("ix_agent_user_id", "user_id"),
    )


# agent bank details
class AgentBankDetails(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    agent_id = db.Column(db.String(50), db.ForeignKey("agent.id"), nullable=False)
    bank_code = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    account_holder_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# commision rate changes record
class CommissionRateChange(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    agent_id = db.Column(db.String(50), db.ForeignKey("agent.id"), nullable=False)
    old_rate = db.Column(db.Float, default=0.0)
    new_rate = db.Column(db.Float, default=0.0)
    change_date = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index("ix_commission_rate_change_created_at", "created_at"),
        Index("ix_commission_rate_change_updated_at", "updated_at"),
        Index("ix_commission_rate_change_agent_id", "agent_id"),
    )


# agent wallet
class AgentWallet(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    agent_id = db.Column(db.String(50), db.ForeignKey("agent.id"), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


# commision record
class CommissionRecord(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True, default=generate_db_id)
    agent_id = db.Column(db.String(50), db.ForeignKey("agent.id"), nullable=False)
    property_id = db.Column(db.String(50), db.ForeignKey("property.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    record_type = db.Column(db.String(50), default=CommissionRecordType.earn)
    refernce_number = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        Index("ix_commission_record_created_at", "created_at"),
        Index("ix_commission_record_updated_at", "updated_at"),
        Index("ix_commission_record_agent_id", "agent_id"),
        Index("ix_commission_record_property_id", "property_id"),
    )
