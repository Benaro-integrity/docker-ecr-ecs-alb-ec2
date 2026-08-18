from flask import Flask, render_template, jsonify, request
import os
import socket
from datetime import datetime

app = Flask(__name__)

# Simulated in-memory request counter for this specific container
request_count = 0

@app.route('/')
def home():
    global request_count
    request_count += 1
    
    # ECS tasks expose the container short ID as the hostname
    container_id = socket.gethostname()
    
    # Optional: Fetch Availability Zone if injected by ECS container metadata
    az = os.environ.get('AWS_ZONE', 'Unknown AZ')
    
    context = {
        'container_id': container_id,
        'request_count': request_count,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'client_ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'aws_zone': az
    }
    return render_template('index.html', **context)

# Critical endpoint for AWS ALB Target Group health checks
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
