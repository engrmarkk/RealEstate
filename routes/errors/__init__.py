from flask import Blueprint
from flask import render_template

error_blp = Blueprint("error_blp", __name__, template_folder="../../templates", static_folder="../../static")

@error_blp.route("/not-found")
def page_not_found():
    return render_template("error_pages/404.html"), 404

@error_blp.route("/network-error")
def internal_server_error():
    return render_template("error_pages/500.html"), 500

@error_blp.route("/too-many-requests")
def too_many_requests():
    return render_template("error_pages/429.html"), 429

@error_blp.route("/maintenance")
def maintenance():
    return render_template("error_pages/maintenance.html"), 503

@error_blp.route("/unauthorized")
def unauthorized():
    return render_template("error_pages/unauthorized.html"), 401

@error_blp.route("/forbidden")
def forbidden():
    return render_template("error_pages/forbidden.html"), 403
