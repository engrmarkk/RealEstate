from enum import Enum as SQLAlchemyEnum

# property_type = SQLAlchemyEnum('property_type', 'house, apartment, commercial, land')


class PropertyType(SQLAlchemyEnum):
    house = "house"
    apartment = "apartment"
    commercial = "commercial"
    land = "land"


# listing_type = SQLAlchemyEnum('listing_type', 'for sale, for rent')


class ListingType(SQLAlchemyEnum):
    for_sale = "for sale"
    for_rent = "for rent"


# property_status = SQLAlchemyEnum('property_status', 'active, sold, pending')


class PropertyStatus(SQLAlchemyEnum):
    active = "active"
    sold = "sold"
    pending = "pending"


# tour type
class TourType(SQLAlchemyEnum):
    in_person = "in_person"
    virtual = "virtual"


# tour status
class TourStatus(SQLAlchemyEnum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class InquiryStatus(SQLAlchemyEnum):
    pending = "pending"
    responded = "responded"
    closed = "closed"


# commission record type (earn or withdraw)
class CommissionRecordType(SQLAlchemyEnum):
    earn = "earn"
    withdraw = "withdraw"
