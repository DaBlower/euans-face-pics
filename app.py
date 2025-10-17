from flask import Flask, send_file, send_from_directory, redirect, url_for, request
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
import os, random, uuid

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1) # show external ips (not caddy's)

project_root = os.path.dirname(__file__)

IMAGE_FOLDER = os.path.join(project_root, "images")
CACHE_BUSTER_LOG = os.path.join(project_root, "slack_cache_busters.txt")

load_dotenv()

os.makedirs(IMAGE_FOLDER, exist_ok=True)

@app.route("/euan/random")
@app.route("/euan/random_slack")
def random_euan():
    images = [f for f in os.listdir(IMAGE_FOLDER)
             if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
    
    if not images:
        mail = os.getenv("dev_email")
        return f"""sorry, there aren't any images (aka something went horribly wrong), please contact <a href="mailto:{mail}">{mail}</a>""", 404
    
    user_agent = request.headers.get("User-Agent", "")
    cache_buster = request.args.get("cache_buster")

    if cache_buster and "Slackbot" in user_agent:
        # Track Slack cache busting tokens for debugging CDN behavior.
        with open(CACHE_BUSTER_LOG, "a", encoding="utf-8") as log_file:
            log_file.write(f"{cache_buster}\n")

    chosen = random.choice(images)
    unique_id = uuid.uuid4()

    return redirect(url_for('serve_img', image_name=chosen, uuid=unique_id, _external=True))


@app.route("/euan/img/<uuid>/<image_name>")
def serve_img(uuid, image_name):
    path = os.path.join(IMAGE_FOLDER, image_name)
    return send_file(path, mimetype="image/*")

@app.route("/euan/count")
def count_euan():
    return str(len(os.listdir(IMAGE_FOLDER)))

@app.route("/")
def demo():
    return send_from_directory(app.static_folder, "demo.html")

if __name__ == "__main__":
    app.run()