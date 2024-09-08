from airflow.decorators import task
from airflow.models.dag import DAG
from airflow.utils.dates import days_ago

from utils.logger_util import logger
from utils.slack_util import success_exit

default_args = {
    "owner": "Engineering Team",
    "start_date": days_ago(1),
}

with DAG(
    dag_id="eng_dag_backfill_li_job_requisition_number_of_cancelled_candidates",
    default_args=default_args,
    description="Backfill job requisition number of cancelled candidates",
    catchup=False,
    schedule_interval=None,
    tags=[
        "eng",
        "backfill",
        "live interview",
        "job requisition",
        "number of cancelled candidates",
    ],
) as dag:

    @task
    def task_sum_backfilling_and_success_exit(
        number_of_job_requisitions_backfilled_list,
    ):
        total_number_of_job_requisitions_backfilled = sum(
            number_of_job_requisitions_backfilled_list
        )
        logger.info(
            f"Total number of job requisitions backfilled: {total_number_of_job_requisitions_backfilled}"
        )
        return success_exit()

    @task
    def task_backfill_li_job_requisitions_number_of_cancelled_candidates_in_batch(
        job_requisition_ids,
    ):
        li_backfill_job_requisitions_number_of_cancelled_candidates_in_batch(
            job_requisition_ids
        )
        return len(job_requisition_ids)

    job_requisition_ids_batches = get_job_requisition_ids_batches(
        {"numberOfCancelledCandidates": {"$exists": False}}
    )

    # this will split whole task into multiple sub-tasks and run in parallel
    backfill_job_requisitions = task_backfill_li_job_requisitions_number_of_cancelled_candidates_in_batch.expand(
        job_requisition_ids=job_requisition_ids_batches
    )

    task_sum_backfilling_and_success_exit(backfill_job_requisitions)
