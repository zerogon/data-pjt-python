import json
import mysql.connector
from kafka import KafkaConsumer
from datetime import datetime

# Kafka Consumer 설정
KAFKA_SERVER = '43.203.170.139:9092'
KAFKA_TOPIC = 'bank_changes.task.bank'
KAFKA_GROUP_ID = 'test-consumer-group'

# MySQL 연결 설정
MYSQL_HOST = 'database-1.ccjsm9pgyenr.ap-northeast-2.rds.amazonaws.com'
MYSQL_DB = 'task'
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'dkansk123'

def save_to_mysql(data, operation):
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            database=MYSQL_DB,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        print("data:", data)
        print("data[registered_at]:", data['registered_at'])

        date_str =  data['registered_at']
        dt_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')

        # 원하는 형식으로 변환
        formatted_date = dt_obj.strftime('%Y%m%d')

        cursor = connection.cursor()
        if operation in ["i", "u", "d"]:
            query = "INSERT INTO bank_history (std_dt, user_id, account, operation_type) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (formatted_date, data['user_id'], data['account'], operation))
        connection.commit()

        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")

def process_kafka_messages():
    # Kafka Consumer 설정
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_SERVER,
            group_id=KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Kafka에서 받은 메시지를 JSON 형식으로 처리
        )

        # 메시지 처리 루프
        for message in consumer:
            print("3")
            print(f"Received message: {message.value}")

            # Kafka 메시지에서 실제 데이터 추출
            event = message.value

            # Debezium 메시지에서 변경사항 가져오기
            
            operation = event['payload']['op']
            after_data = event.get('payload', {}).get('after', {})
            before_data = event.get('payload', {}).get('before', {})

            if operation == "i":  # Insert 작업 처리
                data = after_data
            elif operation == "u":  # Update 작업 처리
                data = after_data
            elif operation == "d":  # Delete 작업 처리
                data = before_data
            else:
                continue  # `op`가 insert, update, delete 외에 다른 값일 때는 무시

            # MySQL에 저장
            save_to_mysql(data, operation)
    except Exception as e:
        print("err message: ",e)
if __name__ == "__main__":
    print("1")
    process_kafka_messages()
