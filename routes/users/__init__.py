from flask import Blueprint

users_blp = Blueprint("users_blp", __name__, template_folder="../../templates", static_folder="../../static")

from .authorized_route import *
from .non_authorized_route import *
