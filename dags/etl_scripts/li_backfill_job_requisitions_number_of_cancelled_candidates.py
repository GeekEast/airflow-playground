import traceback

from dags.eng.core_li.etl_scripts.apis.core_li_job_requisition_apis import (
    recalculate_job_requisition_status,
)
from dags.eng.core_li.etl_scripts.config import REGION_SHORT, STAGE
from utils.logger_util import logger


def li_backfill_job_requisitions_number_of_cancelled_candidates_in_batch(
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
