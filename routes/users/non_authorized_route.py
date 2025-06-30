from . import users_blp
from flask import render_template


@users_blp.route("/")
def homepage():
    return render_template("homepage.html")


# properties
@users_blp.route("/properties")
def properties():
    return render_template("properties.html")


# property
@users_blp.route("/property/<int:property_id>")
def property(property_id):
    print(property_id)
    return render_template("property.html")
