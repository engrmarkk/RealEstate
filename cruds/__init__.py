from models import Users, UserProfile
from extensions import db


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
    return Users.query.filter_by(phone=phone).first()


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
