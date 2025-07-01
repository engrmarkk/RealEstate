from . import authentication_blp
from flask import render_template, request, session, redirect, url_for
from cruds import get_user_by_email, create_user_at_register
from utils.util import (
    validate_correct_email,
    session_alert_bg_color,
    validate_fullname,
    validate_password,
    save_name_email_pass,
)
from flask_login import login_user, login_required, logout_user


@authentication_blp.route("/register", methods=["GET", "POST"])
def register():
    try:
        alert, bg_color = session_alert_bg_color()
        name, email, password, confirm_password = save_name_email_pass(get=True)
        if request.method == "POST":
            email = request.form.get("email")
            fullname = request.form.get("name")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            email_res = validate_correct_email(email)
            if not email_res[0]:
                save_name_email_pass(fullname, email, password, confirm_password)
                session_alert_bg_color(email_res[1])
                return redirect(url_for("authentication_blp.register"))
            if not validate_fullname(fullname):
                save_name_email_pass(fullname, email, password, confirm_password)
                session_alert_bg_color(
                    "Full name must be in the format 'Last Name, First Name'"
                )
                return redirect(url_for("authentication_blp.register"))

            pass_res = validate_password(password)
            if pass_res:
                save_name_email_pass(fullname, email, password, confirm_password)
                session_alert_bg_color(pass_res)
                return redirect(url_for("authentication_blp.register"))

            if password != confirm_password:
                save_name_email_pass(fullname, email, password, confirm_password)
                session_alert_bg_color("Passwords do not match")
                return redirect(url_for("authentication_blp.register"))

            email = email_res[1]

            user = get_user_by_email(email)
            if user:
                save_name_email_pass(fullname, email, password, confirm_password)
                # user already exists
                session_alert_bg_color("Email already exists")
                return redirect(url_for("authentication_blp.register"))

            create_user_at_register(email, password, fullname)
            print("user created")
            session_alert_bg_color("Registration successful, please login", "green")
            return redirect(url_for("authentication_blp.login"))
        return render_template(
            "register.html",
            alert=alert,
            bg_color=bg_color,
            name=name,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )
    except Exception as e:
        print(e, "register error")
        return render_template("register.html")


@authentication_blp.route("/login", methods=["GET", "POST"])
def login():
    alert, bg_color = session_alert_bg_color()
    _, email, password, _ = save_name_email_pass(get=True)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        email_res = validate_correct_email(email)
        if not email_res[0]:
            session_alert_bg_color(email_res[1])
            save_name_email_pass(email=email, password=password)
            return redirect(url_for("authentication_blp.login"))
        email = email_res[1]
        user = get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user, remember=True)
            session_alert_bg_color(f"Welcome, {user.user_profile.first_name}", "green")
            if user.is_admin:
                return redirect(url_for("admin_blp.dashboard"))
            return redirect(url_for("users_blp.homepage"))
        else:
            session_alert_bg_color("Invalid email or password")
            save_name_email_pass(email=email, password=password)
            return redirect(url_for("authentication_blp.login"))
    return render_template(
        "login.html", alert=alert, bg_color=bg_color, email=email, password=password
    )


@authentication_blp.route("/logout")
@login_required
def logout():
    logout_user()
    session_alert_bg_color("Logout successful", "green")
    return redirect(url_for("authentication_blp.login"))
