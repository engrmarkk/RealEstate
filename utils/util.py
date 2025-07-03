import uuid
import string
import random
from flask import session
from email_validator import validate_email, EmailNotValidError
from werkzeug.utils import secure_filename
import os


def generate_db_id():
    return str(uuid.uuid4().hex)


# generate agent code
def generate_agent_code():
    gen_code = "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
    )
    return f"AGENT-{gen_code}"


def validate_correct_email(email):
    try:
        # Validate the email
        validated_email = validate_email(email)
        # Normalize the email (e.g., convert to lowercase)
        normalized_email = validated_email.email
        return True, normalized_email
    except EmailNotValidError as e:
        # Handle invalid email
        return False, str(e)


def session_alert_bg_color(alert=None, bg_color="red"):
    try:
        if alert:
            session["alert"] = alert
            session["bg_color"] = bg_color
            return
        else:
            alert = session.pop("alert", None)
            bg_color = session.pop("bg_color", None)
        return alert, bg_color
    except Exception as e:
        print(e)


# validate fullname
def validate_fullname(fullname):
    if len(fullname.split()) == 2:
        return True
    else:
        return False


# validate password
def validate_password(password):
    """
    :param password:
    :return:

    TODO:
    - length must be at least 8
    - must contain at least one lowercase letter
    - must contain at least one uppercase letter
    - must contain at least one digit
    """
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter"

    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter"

    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit"

    return None


# validate nigeria phone number
def validate_phone_number(phone_number):
    if not phone_number.startswith("0"):
        return "Your phone number must start with 0"
    if not len(phone_number) == 11:
        return "Your phone number must be 11 digits"
    if not phone_number.isdigit():
        return "Your phone number must be a number"
    return None


def format_datetime(date_time):
    return date_time.strftime("%d-%b-%Y")


def save_name_email_pass(
    name="", email="", password="", confirm_password="", get=False
):
    if get:
        name = session.pop("name", "")
        email = session.pop("email", "")
        password = session.pop("password", "")
        confirm_password = session.pop("confirm_password", "")
        return name, email, password, confirm_password
    session["name"] = name
    session["email"] = email
    session["password"] = password
    session["confirm_password"] = confirm_password
    return


def convert_image_to_file(img):
    from werkzeug.utils import secure_filename

    # Get the absolute path to the static/uploads directory
    STATIC_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
    os.makedirs(STATIC_FOLDER, exist_ok=True)  # Ensure the folder exists

    filename = secure_filename(img.filename)
    save_path = os.path.join(STATIC_FOLDER, filename)
    img.save(save_path)

    return save_path
