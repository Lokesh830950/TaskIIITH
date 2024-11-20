import re
import base64
import json
import pandas as pd
from datetime import datetime

def parse_iot_logs(file_path):
    data = []
    base64_pattern = re.compile(r'BASE64:([A-Za-z0-9+/=]+)')
    error_pattern = re.compile(r'(IndexOutOfBoundsException|TimeoutError|InvalidBase64): (.*)')

    with open(file_path, 'r') as file:
        for line in file:
            # Check for Base64 logs
            base64_match = base64_pattern.search(line)
            if base64_match:
                decoded_data = decode_base64(base64_match.group(1))
                data.append(decoded_data)
                continue  # Skip to next line after decoding

            # Check for error logs
            error_match = error_pattern.search(line)
            if error_match:
                error_info = {
                    'timestamp': extract_timestamp(line),
                    'error_type': error_match.group(1),
                    'message': error_match.group(2),
                }
                data.append(error_info)
                continue  # Skip to next line after processing error

            # Check for JSON structured logs
            try:
                if line.startswith('{') and line.endswith('}\n'):
                    json_data = json.loads(line.strip())
                    parsed_data = {
                        'user': json_data.get('user'),
                        'timestamp': json_data.get('timestamp'),
                        'ip': json_data.get('ip'),
                        'event': json_data.get('event'),
                        'item_id': json_data.get('details', {}).get('item_id'),
                        'quantity': json_data.get('details', {}).get('quantity'),
                        'price': json_data.get('details', {}).get('price')
                    }
                    data.append(parsed_data)
            except json.JSONDecodeError:
                continue  # Skip invalid JSON logs

    # Convert to DataFrame for structured representation
    return pd.DataFrame(data)

def decode_base64(encoded_str):
    try:
        # Decode Base64 data and attempt to parse it as JSON if possible
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)
    except (base64.binascii.Error, json.JSONDecodeError):
        return {'Base64Error': 'Invalid Base64 or decoding error'}

def extract_timestamp(line):
    timestamp_pattern = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}')
    match = timestamp_pattern.search(line)
    return match.group(0) if match else None
