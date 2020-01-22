from flask import Flask, jsonify, request
import json
import sys

from faiss_knn import *

app = Flask(__name__)

@app.route('/knn')
def knn():
    id = str(request.args.get('id'))
    count = int(request.args.get('count'))
    result = search_knn(id, count)
    return json.dumps(result)

host = sys.argv[1]
port = int(sys.argv[2])

app.run(host=host, port=port, debug=False)
