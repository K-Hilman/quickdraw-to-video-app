from flask import Flask, render_template, request, jsonify, url_for
import os
import threading
import uuid
from quick_draw import qd_vid, qd
from progress_store import progress_store

app = Flask(__name__)

# Dynamically set SERVER_NAME for background threads
server_name = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if server_name:
    app.config["SERVER_NAME"] = server_name
    app.config["PREFERRED_URL_SCHEME"] = "https"
else:
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["PREFERRED_URL_SCHEME"] = "http"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.join(BASE_DIR, 'static', 'quick_draw')

OUTPUT_DIR = os.path.join(current_dir, "static", "quick_draw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

COUNTRY_LIST = [
    ('AE', 'United Arab Emirates'),
    ('AR', 'Argentina'),
    ('AU', 'Australia'),
    ('BD', 'Bangladesh'),
    ('BR', 'Brazil'),
    ('CA', 'Canada'),
    ('CH', 'Switzerland'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CO', 'Colombia'),
    ('DE', 'Germany'),
    ('EG', 'Egypt'),
    ('ES', 'Spain'),
    ('FR', 'France'),
    ('GB', 'United Kingdom'),
    ('HK', 'Hong Kong'),
    ('ID', 'Indonesia'),
    ('IN', 'India'),
    ('IT', 'Italy'),
    ('JP', 'Japan'),
    ('KR', 'South Korea'),
    ('MX', 'Mexico'),
    ('MY', 'Malaysia'),
    ('NG', 'Nigeria'),
    ('NL', 'Netherlands'),
    ('PH', 'Philippines'),
    ('PK', 'Pakistan'),
    ('PL', 'Poland'),
    ('RO', 'Romania'),
    ('RU', 'Russia'),
    ('SA', 'Saudi Arabia'),
    ('SE', 'Sweden'),
    ('SG', 'Singapore'),
    ('TH', 'Thailand'),
    ('TR', 'Turkey'),
    ('TW', 'Taiwan'),
    ('UA', 'Ukraine'),
    ('US', 'United States'),
    ('VN', 'Vietnam'),
    ('ZA', 'South Africa')
]

@app.route('/')
def index():
    categories = sorted(qd.drawing_names)
    return render_template('index.html', categories=categories, countries=COUNTRY_LIST)

@app.route('/generate', methods=['POST'])
def generate():
    category = request.form.get('category')
    country = request.form.get('country')
    ratio = request.form.get('ratio')
    seed = request.form.get('seed')
    seed_val = int(seed) if seed else None
    jobid = str(uuid.uuid4())
    filename = f"{category}_{country}_{ratio}_{jobid}.mp4"
    outfile = os.path.join('static', 'quick_draw', filename)

    # Mark job as "started"
    progress_store.set(jobid, {'percent': 0, 'status': 'working'})

    # Start background worker
    def worker():
        try:
            def cb(progress):
                percent = int(progress * 100)
                progress_store.set(jobid, {'percent': percent, 'status': 'working'})
            qd_vid(category, country, ratio, seed_val, progress_callback=cb, outfile=outfile)
            # When done:
            with app.app_context():
                progress_store.set(jobid, {
                    'percent': 100,
                    'status': 'finished',
                    'video_url': url_for('static', filename=f'quick_draw/{filename}', _external=True)
                })
        except Exception as ex:
            progress_store.set(jobid, {'percent': 0, 'status': 'error', 'error': str(ex)})

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"jobid": jobid})

@app.route('/progress/<jobid>')
def progress(jobid):
    return jsonify(progress_store.get(jobid))

if __name__ == '__main__':
    app.run(debug=True)