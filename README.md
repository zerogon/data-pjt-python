# 프로젝트 개요
**목표:** 웹사이트의 로그 데이터를 수집, 정제, 처리하여 일일/월간 트래픽 패턴을 분석

## 파이프라인 구성 요소
### 1. 데이터 수집

* 웹사이트 로그 데이터를 수집하는 단계입니다. 가상의 웹사이트 로그 데이터를 주기적으로 수집한다고 가정합니다. 이를 위해 Airflow의 DAG를 활용해 수집 작업을 자동화할 수 있습니다.
### 2. 데이터 저장

* 수집된 로그 데이터를 Hadoop HDFS에 저장합니다. 대용량 데이터를 처리하는 경우, HDFS는 데이터를 분산 저장하고 병렬 처리가 가능하여 유리합니다.
### 3. 데이터 처리 및 변환

* Spark를 활용하여 HDFS에 저장된 로그 데이터를 전처리 및 변환합니다. 예를 들어, 로그 데이터를 파싱하여 필요한 필드를 추출하고, 방문 시간, URL, 방문자 IP 등을 기준으로 필터링할 수 있습니다.
Spark SQL을 사용하여 정제된 데이터를 쿼리하거나 요약할 수 있습니다.
### 4. 데이터 집계 및 분석

* Spark를 이용하여 집계 작업을 수행합니다. 예를 들어, 시간대별 방문자 수를 계산하거나, 인기 페이지를 분석할 수 있습니다.
주기적으로 집계된 결과를 저장해 두고, 일일/월간 트래픽 보고서를 생성할 수 있도록 합니다.
### 5. 파이프라인 자동화

* 전체 과정을 자동화하기 위해 Airflow를 사용해 DAG(Directed Acyclic Graph)를 설계합니다.
* 예시 DAG 흐름:
데이터 수집 작업 (Airflow Operator) → HDFS에 데이터 저장 → Spark로 데이터 처리 및 집계 → 결과 저장 및 알림

## 세부 단계 예시
  1. 데이터 수집 (Airflow Operator)
Airflow PythonOperator를 사용하여 가상의 로그 데이터를 정기적으로 수집 및 저장합니다.
  2. HDFS에 저장
Hadoop 클러스터를 구성하고, 수집된 로그 데이터를 HDFS에 저장합니다.
  3. Spark 데이터 처리
PySpark를 통해 로그 데이터를 처리합니다. Spark SQL로 데이터를 집계하거나 데이터프레임을 조작하여 원하는 결과를 도출합니다.
  4. 결과 저장 및 알림
최종 결과를 분석하여 로컬 DB나 다른 스토리지에 저장하고, 결과 요약본을 알림(예: 이메일)으로 발송합니다.
기술 스택
Apache Airflow: 워크플로우 자동화 및 스케줄링
Apache Hadoop (HDFS): 분산 저장 시스템
Apache Spark: 데이터 처리 및 집계
Python, Spark SQL: 데이터 전처리 및 분석
