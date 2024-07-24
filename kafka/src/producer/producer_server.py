from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from kafka import KafkaProducer
import json
import os

# config.json 파일의 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리 경로
config_path = os.path.join(current_dir, '..', 'config.json')  # 상위 디렉토리의 config.json 경로

# 설정 파일을 읽어서 서버 주소 가져오기
with open(config_path, 'r') as f:
    config = json.load(f)
    server_address = config.get('kafka', {}).get('kafka_server', 'localhost:9092')


# Kafka 프로듀서 설정
producer = KafkaProducer(
    bootstrap_servers=server_address,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic, data):
    producer.send(topic, data)
    producer.flush()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # URL에서 쿼리 매개변수 파싱
        parsed_path = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_path.query)

        color = query_params.get('color', [None])[0]
        user = query_params.get('user', [None])[0]

        if not color or not user:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing parameters")
            return

        # Kafka로 보낼 데이터 생성
        data = {
            'color': color,
            'user': user
        }

        # Kafka로 데이터 전송
        send_to_kafka('hello.kafka', data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data sent to Kafka")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

