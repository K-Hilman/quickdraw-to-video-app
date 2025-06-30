from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
import os

from quick_draw import qd_vid,qd

app = Flask(__name__)

# These would be your previously defined functions:
# qd_gif, qd_vid, etc.

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

    # Run your function (do error checking here too)
    # This will generate a video at static/quick_draw/{category}_{country}_{ratio}.mp4
    qd_vid(category, country, ratio, seed_val)
    filename = f"{category}_{country}_{ratio}.mp4"
    video_url = url_for('static', filename=f'quick_draw/{filename}')
    return jsonify({"video_url": video_url})

if __name__ == '__main__':
    app.run(debug=True)