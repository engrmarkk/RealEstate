import os
from models import PropertyImages, Property
from extensions import db
from services.cloudnary import upload_image
from logger import logger
from workers.utils.cel_workers import celery, shared_task, send_mail
from datetime import datetime


@shared_task
def save_property_images(property_id, images, title):
    logger.info(f"Saving property images: {property_id}, {images}")
    # if the title has whitespaces, replace with underscores
    title = title.replace(" ", "_")
    for image in images:
        image_url = upload_image(image, title=title)
        logger.info(f"Image URL: {image_url} for image: {image}")
        property_image = PropertyImages(image_url=image_url, property_id=property_id)
        db.session.add(property_image)
        # Delete the file after upload
        try:
            os.remove(image)
            logger.info(f"Deleted local file: {image}")
        except Exception as e:
            logger.error(f"Error deleting file {image}: {e}")
    db.session.commit()
    return "Images saved successfully"


@shared_task
def verify_paystack_transaction(user_id, ref):
    try:
        from services.paystack import pay_stack
        from cruds import process_cart_payment, add_to_cart, get_user_carts

        # from workers.utils.cel_workers import send_mail

        res = pay_stack.verify_transaction(ref)
        if res[1] == 200:
            process_cart_payment(user_id, res[0].get("data"))
            user_carts = get_user_carts(user_id)
            carts = [
                {
                    "title": cart.property.title,
                    "property_type": cart.property.property_type.value.title(),
                    "amount": cart.property.price * cart.count,
                    "value": (
                        f"{cart.count} plot(s)"
                        if cart.property.property_type.value == "land"
                        else f"{cart.count} unit(s)"
                    ),
                }
                for cart in user_carts
            ]
            send_mail(
                {
                    "email": user_carts[0].user.email,
                    "subject": "Your payment is successful",
                    "template_name": "receipts.html",
                    "carts": carts,
                    "full_name": f"{user_carts[0].user.user_profile.last_name} {user_carts[0].user.user_profile.first_name}",
                    "total_amount": sum(
                        [cart.property.price * cart.count for cart in user_carts]
                    ),
                    "date": datetime.now().strftime("%d %b, %Y"),
                    "year": datetime.now().strftime("%Y"),
                }
            )
            add_to_cart(user_id, "", "clear_all")
            return True
        return False
    except Exception as e:
        logger.error(f"Error verifying transaction: {e}")
        logger.exception(e)
        return False
