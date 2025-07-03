import cloudinary
import cloudinary.uploader
import cloudinary_config
from constants import CLOUDINARY_UPLOAD_FOLDER


def upload_image(f, title=None):
    upload_options = {
        "folder": CLOUDINARY_UPLOAD_FOLDER,
    }
    if title:
        upload_options["folder"] = f"{CLOUDINARY_UPLOAD_FOLDER}/{title}"
    result = cloudinary.uploader.upload(f, **upload_options)
    image_url = result["secure_url"]
    return image_url
