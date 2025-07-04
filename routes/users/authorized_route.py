from . import users_blp
from flask import render_template, request, jsonify, redirect, url_for
from utils.util import session_alert_bg_color
from cruds import favorite_property, add_to_cart, get_user_carts, \
get_redis_cart_count, fetch_transactions, get_property_purchases, get_one_trans
from flask_login import login_required, current_user
from constants import PAYSTACK_PUBLIC_KEY
from logger import logger


@users_blp.route("/dashboard")
@login_required
def dashboard():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    transactions = fetch_transactions(current_user.id, page, per_page)
    property_purchases = get_property_purchases(current_user.id, page, per_page)
    alert, bg_color = session_alert_bg_color()
    transactions_dicts = [txn.to_dict() for txn in transactions.items]
    return render_template("dashboard.html", alert=alert, bg_color=bg_color, transactions=transactions,
                           transactions_json=transactions_dicts, property_purchases=property_purchases)


# one transaction
@users_blp.route("/transaction/<string:transaction_id>")
@login_required 
def transaction(transaction_id):
    transaction = get_one_trans(current_user.id, transaction_id)
    return render_template("transaction.html", transaction=transaction)


# favourite and unfavourite a property
@users_blp.route("/favourite/<string:property_id>")
@login_required
def favourite(property_id):
    res = favorite_property(current_user.id, property_id)
    return (
        jsonify(
            {
                "success": res,
            }
        ),
        200,
    )


# add to cart
@users_blp.route("/add-to-cart/<string:property_id>/<string:action>")
@login_required
def add_property_to_cart(property_id, action):
    res = add_to_cart(current_user.id, property_id, action)
    return jsonify(res), 200


@users_blp.route("/update-cart-count/<string:property_id>/<string:action>")
@login_required
def update_cart_count(property_id, action):
    add_to_cart(current_user.id, property_id, action)
    return redirect(url_for("users_blp.cart"))


# cart
@users_blp.route("/cart")
@login_required
def cart():
    alert, bg_color = session_alert_bg_color()
    alert_message = request.args.get("alert_message")
    carts = get_user_carts(current_user.id)
    toatl_price = sum([cart.property.price * cart.count for cart in carts])
    return render_template(
        "cart.html",
        carts=carts,
        cart_count=get_redis_cart_count(current_user.id),
        total_price=toatl_price,
        paystack_public_key=PAYSTACK_PUBLIC_KEY,
        alert=alert,
        bg_color=bg_color,
        alert_message=alert_message,
    )


# payment verify
@users_blp.route("/payment/verify")
@login_required
def payment_verify():
    try:
        from workers.background_tasks import verify_paystack_transaction

        reference = request.args.get("reference")
        if not reference:
            return jsonify({"success": False}), 200
        verify_paystack_transaction.delay(current_user.id, reference)
        alert_message = "Transaction in progress"
        return redirect(url_for("users_blp.cart", alert_message=alert_message))
    except Exception as e:
        logger.error(f"Error verifying transaction: {e}")
        logger.exception(e)
        session_alert_bg_color("Payment failed", "red")
        return redirect(url_for("users_blp.cart"))
