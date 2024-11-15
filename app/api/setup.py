from flask import Flask, jsonify, Blueprint, request

from app.scraper.scraper import scrape
from app.scraper.utils import get_html
from app.ntg import predict_review

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Genuine Reviews API v1.0'


@app.route('/scrape')
def scrape_route():
    try:
        req = request.get_json()
    except:
        req = {}

    if 'url' in request.args:
        url = request.args['url']
    else:
        url = req.get('url', '')

    if 'n' in request.args:
        n = request.args['n']
    else:
        n = req.get('n', 20)

    if url == '':
        return jsonify({'message': 'URL is required'}), 400

    res = scrape(url, n)

    print("Got results: ", res)
    comments = [i['body'] for i in res['reviews']]

    predicted = predict_review(comments)

    for i, review in enumerate(res['reviews']):
        review['fake'] = predicted[i]

    if not res:
        return jsonify({'message': 'Invalid URL'}), 400

    return jsonify(res), 200


def run_debug():
    app.run(debug=True)
