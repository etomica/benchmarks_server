import json
import os
import re

from flask.json import jsonify

from benchmarks_server import app

RESULTS_DIR = 'results'


@app.route('/')
def index():
    return "hello world"


@app.route('/results')
def results():
    return jsonify(get_results())


def get_results():
    json_names = [f for f in os.listdir(RESULTS_DIR) if f.endswith('.json')]

    all_results = []
    for fname in json_names:
        date, githash = re.split('[_.]', fname)[:2]

        with open(os.path.join(RESULTS_DIR, fname)) as file:
            benchmarks = json.load(file)
            result = {
                "date": date,
                "commit": githash,
                "benchmarks": benchmarks
            }

            all_results.append(result)

    return all_results

