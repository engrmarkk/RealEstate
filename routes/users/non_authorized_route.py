from . import users_blp
from flask import render_template, request
from utils.util import session_alert_bg_color
from cruds import (
    get_all_properties,
    get_one_property,
    is_favorited,
    get_redis_cart_count,
    get_latest_properties
)
from flask_login import current_user


@users_blp.route("/")
def homepage():
    properties = get_latest_properties()
    return render_template("homepage.html", properties=properties)


# properties
@users_blp.route("/properties")
def properties():
    alert, bg_color = session_alert_bg_color()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    cart_count = 0
    property_type = request.args.get("property_type")
    property_status = request.args.get("property_status")
    city = request.args.get("city")
    state = request.args.get("state")
    properties, total_properties = get_all_properties(
        page, per_page, property_type, property_status, city, state
    )
    if current_user.is_authenticated:
        cart_count = get_redis_cart_count(current_user.id)
    return render_template(
        "properties.html",
        alert=alert,
        bg_color=bg_color,
        properties=properties,
        total_properties=total_properties,
        cart_count=cart_count,
    )


# property
@users_blp.route("/property/<string:property_id>")
def property(property_id):
    alert, bg_color = session_alert_bg_color()
    one_property = get_one_property(property_id)
    image_urls = [img.image_url for img in one_property.property_images]
    is_favorite = False
    cart_count = 0
    if current_user.is_authenticated:
        is_favorite = is_favorited(current_user.id, property_id)
        cart_count = get_redis_cart_count(current_user.id)
    return render_template(
        "property.html",
        alert=alert,
        bg_color=bg_color,
        property=one_property,
        property_images=image_urls,
        is_favorited=is_favorite,
        cart_count=cart_count,
    )
