from models import (
    Users,
    UserProfile,
    Agent,
    AgentBankDetails,
    AgentWallet,
    Property,
    LandDetails,
)
from models.model_enum import PropertyType
from extensions import db
from logger import logger
from utils.util import generate_agent_code


def save_and_commit(obj):
    db.session.add(obj)
    db.session.commit()
    return obj


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
