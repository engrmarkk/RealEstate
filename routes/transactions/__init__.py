from flask import Blueprint

transactions_blp = Blueprint(
    "transactions_blp",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)

from .route import *
