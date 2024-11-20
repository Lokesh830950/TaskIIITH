from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import pandas as pd
from parsers.parser import parse_iot_logs
from parsers.base64_decoder import decode_base64_images
from parsers.web_log_parser import parse_web_server_logs

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DECODED_IMAGES_FOLDER = 'static/images'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECODED_IMAGES_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if file.filename.endswith('.log'):
        parsed_data = parse_iot_logs(file_path)
        decoded_images = decode_base64_images(parsed_data, DECODED_IMAGES_FOLDER)
        web_logs = parse_web_server_logs(file_path)

        # Save parsed data to CSV for visualization
        parsed_data.to_csv('parsed_data.csv', index=False)
        return render_template('data_view.html', data=parsed_data.to_html(), images=decoded_images, web_logs=web_logs)

    return redirect(url_for('index'))

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(DECODED_IMAGES_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
