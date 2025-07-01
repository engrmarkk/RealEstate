from constants import MAINTENANCE_MODE
from flask import redirect, request, url_for

EXCLUDED_ENDPOINTS = ["error_blp.maintenance"]
EXCLUDED_BLUEPRINTS = ["admin_blp", "error_blp"]

def maintenance_check():
    if not MAINTENANCE_MODE:
        return

    if request.blueprint in EXCLUDED_BLUEPRINTS or request.endpoint in EXCLUDED_ENDPOINTS:
        return  # allow error_blp routes

    return redirect(url_for("error_blp.maintenance"))
