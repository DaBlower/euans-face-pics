from flask import Flask, send_file
import os
import random

app = Flask(__name__)

project_root = os.path.dirname(__file__)

IMAGE_FOLDER = os.path.join(project_root, "images")

@app.route("/random_euan")
def random_euan():
    images = [f for f in os.listdir(IMAGE_FOLDER)
             if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    
    if not images:
        return "sorry, there aren't any images (aka something went horribly wrong), please contact obob@duck.com", 404
    
    chosen = random.choice(images)

    return send_file(os.path.join(IMAGE_FOLDER, chosen), mimetype="image/*")
