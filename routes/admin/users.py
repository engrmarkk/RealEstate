from . import admin_blp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from utils.util import session_alert_bg_color
from cruds import get_all_users
from logger import logger


@admin_blp.route("/dashboard")
@login_required
def dashboard():
    alert, bg_color = session_alert_bg_color()
    return render_template("admin/dashboard.html", alert=alert, bg_color=bg_color)


# all users stats
@admin_blp.route("/users")
@login_required
def all_users_stats():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        alert, bg_color = session_alert_bg_color()
        users, total_users = get_all_users(page, per_page)
        return render_template(
            "admin/users.html",
            alert=alert,
            bg_color=bg_color,
            users=users,
            total_users=total_users,
        )
    except Exception as e:
        logger.error(f"Error getting all users stats: {e}")
        return render_template(
            "admin/users.html",
            alert=alert,
            bg_color=bg_color,
            users=None,
            total_users=None,
        )
