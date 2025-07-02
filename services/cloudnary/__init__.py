import cloudinary
import cloudinary.uploader
import cloudinary_config


def upload_image(f):
    result = cloudinary.uploader.upload(
        f, transformation=[{"width": 176, "height": 176, "crop": "fill"}]
    )
    image_url = result["secure_url"]
    return image_url
