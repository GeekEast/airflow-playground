import traceback
from airflow.decorators import task, dag
from airflow.utils.dates import days_ago
from dags.etl_scripts.config import REGION_SHORT, STAGE
from dags.etl_scripts.apis.core_li_job_requisition import (
    recalculate_job_requisition_status,
)
from dags.etl_scripts.get_job_requisition_id_batches import (
    get_job_requisition_id_batches,
)
from utils.logger_util import logger


# get all job requisition ids
@task
def task_get_job_requisition_id_batches():
    return get_job_requisition_id_batches({})


@task(max_active_tis_per_dag=100)
def task_backfill_li_job_requisitions_status_in_batch(
    job_requisition_ids,
):
    try:
        # iterate through job_requisition_ids
        for job_requisition_id in job_requisition_ids:
            recalculate_job_requisition_status(
                job_requisition_id=job_requisition_id,
            )
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        raise Exception(
            f"backfill li job requisitions number of cancelled candidates in stage {STAGE} region {REGION_SHORT}"
        )

    return len(job_requisition_ids)


@task
def task_sum_and_success_exit(number_of_job_requisitions_backfilled_list):
    total_number_of_job_requisitions_backfilled = sum(
        number_of_job_requisitions_backfilled_list
    )
    logger.info(
        f"Total number of job requisitions backfilled: {total_number_of_job_requisitions_backfilled}"
    )


@dag(
    dag_id="dag_backfill_li_job_requisition_status_v2",
    default_args={
        "owner": "engineering-tea,",
        "depends_on_past": False,
        "start_date": days_ago(1),
        "email_on_failure": False,
        "email_on_retry": False,
    },
    description="A DAG for triggering backfill job requisition status",
    schedule=None,
)
def dag_backfill_li_job_requisition_status_v2():
    number_of_job_requisitions_backfilled_list = (
        task_backfill_li_job_requisitions_status_in_batch.expand(
            job_requisition_ids=task_get_job_requisition_id_batches()
        )
    )

    task_sum_and_success_exit(number_of_job_requisitions_backfilled_list)


dag_backfill_li_job_requisition_status_v2()
