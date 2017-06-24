import json
import os
import re
from collections import defaultdict

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

    results_by_param = defaultdict(lambda: defaultdict(list))
    dates = []
    commits = []


    for fname in json_names:
        date, githash = re.split('[_.]', fname)[:2]
        dates.append(date)
        commits.append(githash)

        with open(os.path.join(RESULTS_DIR, fname)) as file:
            run_results = json.load(file)
            for bench_result in run_results:
                b = results_by_param[bench_result['benchmark']]
                params = bench_result['params']
                if 'numMolecules' in params.keys():
                    param = params['numMolecules']
                else:
                    param = params['numAtoms']

                score = [
                    bench_result['primaryMetric']['score'],
                    bench_result['primaryMetric']['scoreError']
                ]

                b[param].append(score)

    benchmarks = defaultdict(dict)
    for bench_name, param_results in results_by_param.items():
        keys = [k for k in param_results.keys()]
        keys.sort(key=lambda s: int(s))

        bench = benchmarks[bench_name]
        bench['data'] = [d for d in zip(dates, *[param_results[k] for k in keys])]
        bench['labels'] = ["Date", *keys]

    return {
        "benchmarks": benchmarks,
        "commits": commits
    }
