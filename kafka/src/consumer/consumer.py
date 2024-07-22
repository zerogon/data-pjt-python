import json
import os
from kafka import KafkaConsumer
from hdfs import InsecureClient

# 상위 폴더의 config.json 파일 경로 설정
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

def load_config():
    """config.json 파일 로드 함수"""
    with open(CONFIG_PATH, 'r') as file:
        config = json.load(file)
    return config

def create_kafka_consumer(config):
    """Kafka Consumer 생성 함수"""
    kafka_config = config['kafka']
    consumer = KafkaConsumer(
        'hello.kafka', 
        bootstrap_servers=kafka_config['bootstrap_servers'],
        group_id=kafka_config['group_id'],
        auto_offset_reset='earliest'
    )
    return consumer

def create_hdfs_client(config):
    """HDFS 클라이언트 생성 함수"""
    hdfs_config = config['hdfs']
    client = InsecureClient(hdfs_config['namenode'], user=hdfs_config['user'])
    return client

def consume_messages(consumer, client):
    """Kafka 메시지를 HDFS에 저장하는 함수"""
    try:
        for message in consumer:
            print(f"Received message: {message.value.decode('utf-8')}")
            # HDFS에 메시지 저장
            with client.write('/user/hdfs/output.txt', overwrite=True) as writer:
                writer.write(message.value)
    except KeyboardInterrupt:
        print("Consumer interrupted")
    finally:
        consumer.close()

def main():
    config = load_config()
    consumer = create_kafka_consumer(config)
    client = create_hdfs_client(config)
    consume_messages(consumer, client)

if __name__ == "__main__":
    main()
