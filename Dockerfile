FROM apache/airflow:${AIRFLOW_VERSION}-python3.10
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt