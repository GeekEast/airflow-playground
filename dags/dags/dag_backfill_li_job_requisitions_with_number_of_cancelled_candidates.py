import time
from airflow.decorators import task, dag
from airflow.utils.dates import days_ago
from utils.logger_util import logger
from bson import ObjectId
from airflow.operators.python import get_current_context


@task
def task_get_job_requisition_id_batches():
    # job_requisition_ids = get_job_requisition_ids()
    job_requisition_ids = [str(ObjectId()) for _ in range(1000)]

    return [
        job_requisition_ids[i : i + 100]
        # page size 100
        for i in range(0, len(job_requisition_ids), 100)
    ]


@task(max_active_tis_per_dag=1)
def task_backfill_job_requisitions_with_number_of_cancelled_candidates(
    job_requisition_ids,
):

    for job_requisition_id in job_requisition_ids:
        time.sleep(0.05)
        logger.info(f"Backfilling job requisition with id: {job_requisition_id}")
    return len(job_requisition_ids)


@task
def task_sum(values):
    context = get_current_context()
    logger.info(f"Context: {context}")
    ti = context["ti"]
    logger.info(f"ti: {ti}")

    total_number_of_processed_job_requisitions = sum(values)
    logger.info(
        f"Summing number of processed job requisitions: {total_number_of_processed_job_requisitions}"
    )
    return total_number_of_processed_job_requisitions


@dag(
    dag_id="backfill_li_job_requisitions_with_number_of_cancelled_candidates",
    default_args={
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": days_ago(1),
        "email_on_failure": False,
        "email_on_retry": False,
    },
    description="A DAG for backfilling job requisitions with number of cancelled candidates",
    schedule=None,
)
def dag_backfill_job_requisitions_with_number_of_cancelled_candidates():
    task_backfill_job_requisitions_with_number_of_cancelled_candidates_results = (
        task_backfill_job_requisitions_with_number_of_cancelled_candidates.expand(
            job_requisition_ids=task_get_job_requisition_id_batches()
        )
    )

    task_sum(task_backfill_job_requisitions_with_number_of_cancelled_candidates_results)


dag_backfill_job_requisitions_with_number_of_cancelled_candidates()
