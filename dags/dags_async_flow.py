from airflow.models.dag import DAG
from airflow.utils.dates import days_ago
from etl_scripts.apis.core_li import get_job_requisition_ids
from utils.logger_util import logger
from airflow.decorators import task
from etl_scripts.apis.core_li import update_job_requisition

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email_on_failure": False,
    "email_on_retry": False,
}


def get_job_requisition_batches():
    job_requisition_ids = get_job_requisition_ids()
    total_number_of_records_to_update = len(job_requisition_ids)
    logger.info(
        f"Total number of records to update: {total_number_of_records_to_update}"
    )
    # return 100 job requisition ids at a time
    return [
        job_requisition_ids[i : i + 100]
        for i in range(0, len(job_requisition_ids), 100)
    ]


with DAG(
    dag_id="async_flow",
    default_args=default_args,
    description="A DAG with async operation for backfilling cancelled candidates",
    schedule=None,
) as dag:

    @task
    def task_sum(values):
        logger.info(f"Summing number of process job requisitions: {values}")
        return sum(values)

    @task
    def task_backfill_number_of_cancelled_candidates_in_batch(job_requisition_ids):
        for job_requisition_id in job_requisition_ids:
            update_job_requisition(job_requisition_id)
        return len(job_requisition_ids)

    backfill_job_requisitions = (
        task_backfill_number_of_cancelled_candidates_in_batch.expand(
            job_requisition_ids=get_job_requisition_batches()
        )
    )

    task_sum(backfill_job_requisitions)
