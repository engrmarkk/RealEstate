from models import Users, UserProfile, Agent, AgentBankDetails, AgentWallet
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
