FROM apache/airflow:2.9.2-python3.10
ADD requirements.txt .
RUN pip install -r requirements.txt