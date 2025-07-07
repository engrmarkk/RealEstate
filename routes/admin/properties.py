from . import admin_blp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required
from utils.util import session_alert_bg_color, convert_image_to_file
from logger import logger
from cruds import save_land_property, get_all_properties, get_one_property, save_apartment_property


@admin_blp.route("/properties")
@login_required
def properties():
    alert, bg_color = session_alert_bg_color()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    property_type = request.args.get("property_type")
    property_status = request.args.get("property_status")
    city = request.args.get("city")
    state = request.args.get("state")
    properties, total_properties = get_all_properties(
        page, per_page, property_type, property_status, city, state
    )
    return render_template(
        "admin/properties.html",
        alert=alert,
        bg_color=bg_color,
        properties=properties,
        total_properties=total_properties,
    )


# one property
@admin_blp.route("/view_property/<string:property_id>")
@login_required
def view_property(property_id):
    logger.info(f"Property ID: {property_id}")
    one_property = get_one_property(property_id)
    # Extract image URLs from the property_images relationship/attribute
    image_urls = [
        img.image_url for img in one_property.property_images
    ]  # Adjust 'url' to your actual field name
    return render_template(
        "admin/one_property.html",
        property=one_property,
        property_images=image_urls,  # Pass as a plain list
    )


# add land
@admin_blp.route("/add_land", methods=["GET", "POST"])
@login_required
def add_land():
    alert, bg_color = session_alert_bg_color()
    if request.method == "POST":
        title = request.form.get("title")
        address = request.form.get("address")
        description = request.form.get("description")
        price = request.form.get("price")
        state = request.form.get("state")
        city = request.form.get("city")
        size = request.form.get("size")
        area_sqft = request.form.get("area_sqft")
        images = request.files.getlist("images")
        if not all(
            [title, address, description, price, area_sqft, state, city, size, images]
        ):
            session_alert_bg_color("Please fill in all fields")
            return redirect(url_for("admin_blp.add_land"))
        saved_filenames = [
            convert_image_to_file(img) for img in images if img and img.filename
        ]
        logger.info(f"Saved filenames: {saved_filenames}")
        save_land_property(
            title,
            address,
            description,
            price,
            area_sqft,
            state,
            city,
            size,
            saved_filenames,
        )

        session_alert_bg_color("Land property added successfully", "green")
        return redirect(url_for("admin_blp.properties"))
    return render_template("admin/add_land.html", alert=alert, bg_color=bg_color)


# add apartment
@admin_blp.route("/add_apartment", methods=["GET", "POST"])
@login_required
def add_apartment():
    alert, bg_color = session_alert_bg_color()
    if request.method == "POST":
        title = request.form.get("title")
        address = request.form.get("address")
        description = request.form.get("description")
        price = request.form.get("price")
        state = request.form.get("state")
        city = request.form.get("city")
        bedrooms = request.form.get("bedrooms", "0")
        bathrooms = request.form.get("bathrooms", "0")
        garage_spaces = request.form.get("garage_spaces", "0")
        has_pool = bool(request.form.get("has_pool"))
        has_garden = bool(request.form.get("has_garden"))
        has_balcony = bool(request.form.get("has_balcony"))
        has_elevator = bool(request.form.get("has_elevator"))
        is_furnished = bool(request.form.get("is_furnished"))
        is_pet_friendly = bool(request.form.get("is_pet_friendly"))
        images = request.files.getlist("images")
        listing_type = request.form.get("listing_type")
        if not all(
            [
                title,
                address,
                description,
                price,
                bedrooms,
                bathrooms,
                state,
                city,
                images,
                listing_type
            ]
        ):
            session_alert_bg_color("Please fill in all fields")
            return redirect(url_for("admin_blp.add_apartment"))
        saved_filenames = [
            convert_image_to_file(img) for img in images if img and img.filename
        ]
        logger.info(f"Saved filenames: {saved_filenames}")
        save_apartment_property(
            title,
            address,
            description,
            price,
            state,
            city,
            bedrooms,
            bathrooms,
            garage_spaces,
            has_pool,
            has_garden,
            has_balcony,
            has_elevator,
            is_furnished,
            is_pet_friendly,
            saved_filenames,
            listing_type
        )
        session_alert_bg_color("Apartment property added successfully", "green")
        return redirect(url_for("admin_blp.add_apartment"))
    return render_template("admin/add_apartment.html", alert=alert, bg_color=bg_color)
