import traceback
from airflow.decorators import task, dag
from airflow.utils.dates import days_ago
from dags.etl_scripts.config import STAGE
from dags.etl_scripts.apis.core_li_job_requisition import (
    recalculate_job_requisition_status,
)
from dags.etl_scripts.backfill_job_requisition_status import (
    get_job_requisition_id_batches,
)
from utils.logger_util import logger

from airflow.models.param import Param


# get all job requisition ids
@task
def task_get_job_requisition_id_batches():
    return get_job_requisition_id_batches({})


@task()
def task_backfill_li_job_requisitions_status_in_batch(job_requisition_ids):
    try:
        # iterate through job_requisition_ids
        for job_requisition_id in job_requisition_ids:
            recalculate_job_requisition_status(job_requisition_id=job_requisition_id)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
        raise Exception(
            f"backfill li job requisitions number of cancelled candidates in stage {STAGE}"
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
    dag_id="dag_backfill_li_job_requisition_status",
    default_args={
        "owner": "engineering-team",
        "depends_on_past": False,
        "start_date": days_ago(1),
        "email_on_failure": False,
        "email_on_retry": False,
    },
    description="A DAG for triggering backfill job requisition status",
    schedule=None,
    max_active_tasks=10,
    params={"region": Param("ap-southeast-2", type="string", title="AWS Region")},
)
def dag_backfill_li_job_requisition_status():
    number_of_job_requisitions_backfilled_list = (
        task_backfill_li_job_requisitions_status_in_batch.partial().expand(
            job_requisition_ids=task_get_job_requisition_id_batches(),
        )
    )

    task_sum_and_success_exit(number_of_job_requisitions_backfilled_list)


dag_backfill_li_job_requisition_status()
