import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def save_picture(form_picture, folder='uploads'):
    """
    Saves an uploaded picture to the static/uploads directory.
    Renames file to a random hex string to avoid collisions.
    Resizes image to max 1200px width (optional).
    
    :param form_picture: The file object from the form
    :param folder: subfolder inside static (default: uploads)
    :return: The relative filename
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Create directory if not exists
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    picture_path = os.path.join(upload_path, picture_fn)

    # Resize and Save
    output_size = (1200, 1200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
