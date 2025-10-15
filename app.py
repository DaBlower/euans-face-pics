from flask import Flask, send_file, send_from_directory, redirect, url_for
import os
from dotenv import load_dotenv
import random

app = Flask(__name__)

project_root = os.path.dirname(__file__)

IMAGE_FOLDER = os.path.join(project_root, "images")

load_dotenv()

os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route("/euan/random")
def random_euan():
    images = [f for f in os.listdir(IMAGE_FOLDER)
             if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    
    if not images:
        mail = os.getenv("dev_email")
        return f"""sorry, there aren't any images (aka something went horribly wrong), please contact <a href="mailto:{mail}">{mail}</a>""", 404
    
    chosen = random.choice(images)

    response = send_file(os.path.join(IMAGE_FOLDER, chosen), mimetype="image/*")
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/euan/random_cache_buster")
def random_euan_redirect():
    cache_buster = random.randint(0, 1_000_000_000)
    response = redirect(url_for("random_euan", _external=True, cache_bust=cache_buster))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/euan/count")
def count_euan():
    return str(len(os.listdir(IMAGE_FOLDER)))

@app.route("/")
def demo():
    return send_from_directory(app.static_folder, "demo.html")

if __name__ == "__main__":
    app.run()