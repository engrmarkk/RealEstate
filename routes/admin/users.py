from . import admin_blp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from utils.util import session_alert_bg_color


@admin_blp.route("/dashboard")
@login_required
def dashboard():
    alert, bg_color = session_alert_bg_color()
    return render_template("admin/dashboard.html", alert=alert, bg_color=bg_color)
