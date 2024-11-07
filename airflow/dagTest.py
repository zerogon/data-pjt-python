from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pandas as pd
from datetime import datetime

# MySQL 테이블에 삽입하는 함수
def insert_sales_data_to_mysql():
    file_path = "/data/test_data.csv"
    
    df = pd.read_csv(file_path)
    
    # 데이터 타입에 맞게 변환 (예시)
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['quantity'] = df['quantity'].astype(int)
    
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default') 
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    
    # MySQL에 데이터 삽입
    for _, row in df.iterrows():
        sql = """
            INSERT INTO sales (sale_date, product_id, amount, quantity)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (row['sale_date'], row['product_id'], row['amount'], row['quantity']))
    
    # 트랜잭션 커밋 및 연결 종료
    connection.commit()
    cursor.close()
    connection.close()

# DAG 정의
with DAG(
    dag_id="sales_data_to_mysql",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    # 데이터 삽입 태스크
    insert_data_task = PythonOperator(
        task_id="insert_sales_data_to_mysql",
        python_callable=insert_sales_data_to_mysql
    )

    insert_data_task
