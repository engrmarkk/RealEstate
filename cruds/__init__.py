from models import (
    Users,
    UserProfile,
    Agent,
    AgentBankDetails,
    AgentWallet,
    Property,
    LandDetails,
    HouseDetails,
    Favorite,
    PropertyCart,
    Transaction,
    PropertyPurchased,
)
from models.model_enum import PropertyType, ListingType
from extensions import db
from logger import logger
from utils.util import generate_agent_code
from connections import redis_conn


def save_and_commit(obj):
    db.session.add(obj)
    db.session.commit()
    return obj


def delete_and_commit(obj):
    db.session.delete(obj)
    db.session.commit()
    return False


def get_user_by_email(email):
    return Users.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return Users.query.filter_by(id=user_id).first()


# phone
def get_user_by_phone(phone):
    return UserProfile.query.filter_by(phone=phone).first()


# create user along with user profile
def create_user_at_register(email, password, fullname):
    last_name, first_name = fullname.split()
    user = Users(
        email=email,
        password=password,
        user_profile=UserProfile(first_name=first_name, last_name=last_name),
    )
    save_and_commit(user)
    return user


def create_agent(
    first_name,
    last_name,
    email,
    license_number,
    experience_years,
    commission_rate,
    bank_code,
    account_number,
    account_holder_name,
    bank_name,
    phone,
):
    try:
        user = Users(
            email=email,
            password=first_name.title(),
            user_profile=UserProfile(
                first_name=first_name, last_name=last_name, phone=phone
            ),
            agent=Agent(
                agent_code=generate_agent_code(),
                license_number=license_number,
                experience_years=int(experience_years),
                commission_rate=float(commission_rate),
                is_verified=True,
                agent_bank_details=AgentBankDetails(
                    bank_code=bank_code,
                    account_number=account_number,
                    account_holder_name=account_holder_name,
                    bank_name=bank_name,
                ),
                agent_wallet=AgentWallet(balance=0.0),
            ),
        )
        save_and_commit(user)
        return user
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return None


# get all users that are not agent(that does not have agent table) or admin
def get_all_users(page, per_page):
    try:
        # also get total users count
        users = (
            Users.query.filter(Users.agent == None, Users.is_admin == False)
            .order_by(Users.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        total_users = Users.query.filter(
            Users.agent == None, Users.is_admin == False
        ).count()
        return users, total_users
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        return None, 0


def get_all_agents(page, per_page):
    try:
        agents = (
            Users.query.filter(Users.agent != None)
            .order_by(Users.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        total_agents = Users.query.filter(Users.agent != None).count()
        return agents, total_agents
    except Exception as e:
        logger.error(f"Error getting all agents: {e}")
        return None, 0


# gett ine agent
def get_agent_by_id(agent_id):
    return Users.query.filter_by(id=agent_id).first()


def save_land_property(
    title, address, description, price, area_sqft, state, city, size, images
):
    try:
        from workers.background_tasks import save_property_images

        property = Property(
            title=title,
            address=address,
            description=description,
            price=price,
            state=state,
            city=city,
            property_type=PropertyType.land,
            land_details=LandDetails(size=size, area_sqft=area_sqft),
        )
        property = save_and_commit(property)
        save_property_images.delay(property.id, images, title)
        return property
    except Exception as e:
        logger.error(f"Error saving land property: {e}")
        return None


def save_apartment_property(
    title,
    address,
    description,
    price,
    state,
    city,
    bedrooms,
    bathrooms,
    garage_spaces,
    has_pool,
    has_garden,
    has_balcony,
    has_elevator,
    is_furnished,
    is_pet_friendly,
    images,
    listing_type
):
    try:
        from workers.background_tasks import save_property_images

        property = Property(
            title=title,
            address=address,
            description=description,
            price=price,
            state=state,
            city=city,
            property_type=PropertyType.apartment,
            listing_type=ListingType.for_sale if listing_type == "sale" else ListingType.for_rent,
            house_details=HouseDetails(
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                garage_spaces=garage_spaces,
                has_pool=has_pool,
                has_garden=has_garden,
                has_balcony=has_balcony,
                has_elevator=has_elevator,
                is_furnished=is_furnished,
                is_pet_friendly=is_pet_friendly,
            ),
        )
        property = save_and_commit(property)
        save_property_images.delay(property.id, images, title)
        return property
    except Exception as e:
        logger.error(f"Error saving apartment property: {e}")
        return None


# get properties with filters
def get_all_properties(page, per_page, property_type, property_status, city, state):
    try:
        properties = (
            Property.query.filter(
                Property.property_type == property_type if property_type else True,
                (
                    Property.property_status == property_status
                    if property_status
                    else True
                ),
                Property.state == state if state else True,
                Property.city == city if city else True,
                Property.available == True,
            )
            .order_by(Property.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        total_properties = Property.query.filter(
            Property.property_type == property_type if property_type else True,
            Property.property_status == property_status if property_status else True,
            Property.state == state if state else True,
            Property.city == city if city else True,
        ).count()
        return properties, total_properties
    except Exception as e:
        logger.error(f"Error getting all properties: {e}")
        return None, 0


def get_one_property(property_id):
    return Property.query.filter_by(id=property_id).first()


# fav and un-fav property
def favorite_property(user_id, property_id):
    try:
        favorite = Favorite.query.filter_by(
            user_id=user_id, property_id=property_id
        ).first()
        if favorite:
            return delete_and_commit(favorite)
        favorite = Favorite(user_id=user_id, property_id=property_id)
        save_and_commit(favorite)
        return True
    except Exception as e:
        logger.error(f"Error favoriting property: {e}")
        return None


def is_favorited(user_id, property_id):
    return (
        Favorite.query.filter_by(user_id=user_id, property_id=property_id).first()
        is not None
    )


def get_user_cart_count(user_id):
    count = PropertyCart.query.filter_by(user_id=user_id).count()
    redis_conn.set(f"{user_id}_cart_count", count, 100)
    return count


def get_redis_cart_count(user_id):
    return redis_conn.get(f"{user_id}_cart_count") or 0


# add to cart
def add_to_cart(user_id, property_id, action="add"):
    try:
        prop = Property.query.filter_by(id=property_id).first()
        if action == "remove_all":
            delete_and_commit(
                PropertyCart.query.filter_by(
                    user_id=user_id, property_id=property_id
                ).first()
            )
            return {
                "cart_count": get_user_cart_count(user_id),
            }
        elif action == "remove_one":
            cart = PropertyCart.query.filter_by(
                user_id=user_id, property_id=property_id
            ).first()
            if cart:
                cart.count -= 1
                db.session.commit()
                return {
                    "cart_count": get_user_cart_count(user_id),
                }
            return {
                "cart_count": get_user_cart_count(user_id),
            }
        elif action == "clear_all":
            PropertyCart.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            return {
                "cart_count": get_user_cart_count(user_id),
            }
        else:
            # if the cart exist, and action is True, then add the count
            cart = PropertyCart.query.filter_by(
                user_id=user_id, property_id=property_id
            ).first()
            if cart:
                # if the cart exists and the property is a land, and the cart count is less than the land size
                if prop.land_details and prop.land_details.size > cart.count:
                    cart.count += 1
                    db.session.commit()
                    return {
                        "cart_count": get_user_cart_count(user_id),
                    }
                return {
                    "cart_count": get_user_cart_count(user_id),
                }
            cart = PropertyCart(user_id=user_id, property_id=property_id)
            save_and_commit(cart)
            return {
                "cart_count": get_user_cart_count(user_id),
            }
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return None


# get user carts
def get_user_carts(user_id):
    return (
        PropertyCart.query.join(Property, Property.id == PropertyCart.property_id).filter(
            PropertyCart.user_id == user_id,
            Property.available == True)
        .order_by(PropertyCart.created_at.desc())
        .all()
    )


def save_transaction(data, user_id):
    new_trans = Transaction(
        amount=float(data.get("amount")) / 100,
        user_id=user_id,
        channel=data.get("channel"),
        transaction_id=data.get("id"),
        authorization_dict=data.get("authorization", {}),
        ip_address=data.get("ip_address"),
        reference_number=data.get("reference"),
    )
    save_and_commit(new_trans)
    return new_trans


# property purchased
def save_property_purchased(property_id, user_id, amount, trans_id, count=1):
    new_trans = PropertyPurchased(
        property_id=property_id,
        user_id=user_id,
        amount=amount,
        count=count,
        transaction_id=trans_id,
    )
    save_and_commit(new_trans)
    return new_trans


# get carts
def get_property_carts(user_id):
    return PropertyCart.query.filter_by(user_id=user_id).all()


# reduce count for property purchase
def reduce_land_plot(property_id, count):
    prop = Property.query.filter_by(id=property_id).first()
    land_prop = prop.land_details
    if land_prop:
        land_prop.size -= count
        db.session.commit()
    update_available_status(property_id)
    return


def update_available_status(property_id):
    try:
        prop = Property.query.get(property_id)
        if prop:
            if prop.land_details and prop.land_details.size == 0:
                prop.available = False
            if prop.house_details:
                prop.available = False
            db.session.commit()
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating available status: {e}")
        return False


# proccess cart purchase
def process_cart_payment(user_id, data):
    carts_props = get_property_carts(user_id)
    trans = save_transaction(data, user_id)
    for cart in carts_props:
        save_property_purchased(
            cart.property_id,
            user_id,
            cart.count * cart.property.price,
            trans.id,
            cart.count,
        )
        reduce_land_plot(cart.property_id, cart.count)
    return


# get transactions
def fetch_transactions(user_id, page, per_page):
    return (
        Transaction.query.filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )


def get_one_trans(user_id, transaction_id):
    return (
        Transaction.query.filter(Transaction.user_id == user_id)
        .filter(Transaction.id == transaction_id)
        .first()
    )


def get_property_purchases(user_id, page, per_page):
    return (
        PropertyPurchased.query.filter(PropertyPurchased.user_id == user_id)
        .order_by(PropertyPurchased.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )
