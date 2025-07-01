from models import PropertyImages
from extensions import db
from services.cloudnary import upload_image
from logger import logger
from workers.utils.cel_workers import celery, shared_task, send_mail


@shared_task
def save_property_images(property_id, images):
    logger.info(f"Saving property images: {property_id}, {images}")
    for image in images:
        image_url = upload_image(image)
        logger.info(f"Image URL: {image_url} for image: {image}")
        property_image = PropertyImages(image_url=image_url, property_id=property_id)
        db.session.add(property_image)
    db.session.commit()
    return "Images saved successfully"
