from flask import Blueprint

admin_blp = Blueprint(
    "admin_blp",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)

from .users import *
from .properties import *
from .agents import *
