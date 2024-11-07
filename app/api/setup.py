from flask import Flask, jsonify, Blueprint, request

from app.scraper.scraper import scrape
from app.scraper.utils import get_html

app = Flask(__name__)

api = Blueprint('api', __name__, url_prefix='/api/v1')

@app.route('/')
def hello():
    return 'Genuine Reviews API v1.0'

@api.route('/ping')
def ping():
    return jsonify({'message': 'pong'})

@api.route('/scrape')
def scrape_route():
    if 'url' in request.args:
        url = request.args['url']
    else:
        req = request.get_json()
        url = req['url']
    if url == '':
        return jsonify({'message': 'URL is required'}), 400

    res = scrape(url)
    print(res)

    if not res:
        return jsonify({'message': 'Invalid URL'}), 400

    return res

app.register_blueprint(api)

def run_debug():
    app.run(debug=True)