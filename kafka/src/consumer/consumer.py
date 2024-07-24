import json
import os
from kafka import KafkaConsumer
from hdfs import InsecureClient

# 설정 파일 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)
    kafka_server = config.get('kafka', {}).get('kafka_server', 'localhost:9092')
    hdfs_url = config.get('hdfs', {}).get('hdfs_url', 'http://localhost:50070')
    hdfs_user = config.get('hdfs', {}).get('user', 'ec2-user')

# Kafka 컨슈머 설정
consumer = KafkaConsumer(
    'hello.kafka',
    bootstrap_servers=kafka_server,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='hdfs',  # 그룹 ID 설정
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# HDFS 클라이언트 설정
client = InsecureClient(hdfs_url, user=hdfs_user)

def write_to_hdfs(hdfs_path, data):
    with client.write(hdfs_path, overwrite=True, encoding='utf-8') as writer:
        writer.write(data)

# Kafka 메시지 소비 및 HDFS로 데이터 적재
for message in consumer:
    message_value = message.value
    hdfs_path = '/tmp/output.txt'  # HDFS 경로 설정 (필요에 따라 변경 가능)

    # HDFS에 데이터 쓰기
    write_to_hdfs(hdfs_path, json.dumps(message_value))
    print(f"Data written to HDFS: {message_value}")

# Note: For a real-world application, more sophisticated error handling and logging would be required.
