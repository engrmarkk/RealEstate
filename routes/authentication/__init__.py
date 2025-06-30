from flask import Blueprint

authentication_blp = Blueprint("authentication_blp", __name__)

from .route import *
