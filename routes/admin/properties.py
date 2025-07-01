from . import admin_blp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from utils.util import session_alert_bg_color


@admin_blp.route("/properties")
@login_required
def properties():
    alert, bg_color = session_alert_bg_color()
    return render_template("admin/properties.html", alert=alert, bg_color=bg_color)


# add land
@admin_blp.route("/add_land", methods=["GET", "POST"])
@login_required
def add_land():
    alert, bg_color = session_alert_bg_color()
    return render_template("admin/add_land.html", alert=alert, bg_color=bg_color)
