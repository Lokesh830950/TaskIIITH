import re
from collections import Counter

def parse_web_server_logs(file_path):
    log_pattern = re.compile(r'(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+) (?P<url>\S+) HTTP/\d.\d" (?P<status>\d+)')
    metrics = Counter()

    with open(file_path, 'r') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                metrics['requests'] += 1
                metrics[f'status_{match.group("status")}'] += 1
    
    return metrics
