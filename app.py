from flask import Flask, send_file
import os
from dotenv import load_dotenv
import random

app = Flask(__name__)

project_root = os.path.dirname(__file__)

IMAGE_FOLDER = os.path.join(project_root, "images")

load_dotenv()

os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route("/random_euan")
def random_euan():
    images = [f for f in os.listdir(IMAGE_FOLDER)
             if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    
    if not images:
        mail = os.getenv("dev_email")
        return f"""sorry, there aren't any images (aka something went horribly wrong), please contact <a href="mailto:{mail}">{mail}</a>""", 404
    
    chosen = random.choice(images)

    return send_file(os.path.join(IMAGE_FOLDER, chosen), mimetype="image/*")

if __name__ == "__main__":
    app.run()