from flask import Flask, request, jsonify, send_from_directory
from elasticsearch import Elasticsearch
import json
import os
import datetime

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def json_payload(service_name, service_status, host_name, timestamp):
    script_directory = os.path.dirname(__file__)
    filename = os.path.join(script_directory, f"{service_name}-status-{timestamp}.json")
    data = {
        "service_name": service_name,
        "service_status": service_status,
        "host_name": host_name
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def final_status(service_statuses):
    return "UP" if all(status == "UP" for status in service_statuses) else "DOWN"

@app.route('/add', methods=['POST'])
def add_to_elasticsearch():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and file.filename.endswith('.json'):
            data = json.load(file)
            es.index(index='data', body=data)
            return jsonify({'message': 'Data added to Elasticsearch successfully'}), 201
        else:
            return jsonify({'error': 'Invalid file format. Please upload a JSON file.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
    try:
        script_directory = os.path.dirname(__file__)
        files = [f for f in os.listdir(script_directory) if f.endswith('.json')]
        if not files:
            return jsonify({'error': 'No health check data available'}), 404
        service_statuses = []
        for filename in files:
            with open(os.path.join(script_directory, filename), 'r') as f:
                data = json.load(f)
                service_statuses.append(data['service_status'])
        overall_status = final_status(service_statuses)
        return jsonify({'overall_status': overall_status, 'applications': service_statuses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/healthcheck/<service_name>', methods=['GET'])
def get_specific_healthcheck(service_name):
    try:
        script_directory = os.path.dirname(__file__)
        files = [f for f in os.listdir(script_directory) if f.endswith('.json') and service_name in f]
        
        if not files:
            return jsonify({'error': f'No data found for service: {service_name}'}), 404
        specific_service_statuses = []
        for filename in files:
            with open(os.path.join(script_directory, filename), 'r') as f:
                data = json.load(f)
                specific_service_statuses.append(data['service_status'])
        return jsonify({'service_name': service_name, 'service_statuses': specific_service_statuses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)