import math

from dags.etl_scripts.config import DEFAULT_QUERY_PAGINATION_SIZE
from dags.etl_scripts.apis.core_li_job_requisition import (
    get_job_requisition_ids_with_pagination,
    get_job_requisitions_count,
)
from utils.logger_util import logger


# should return [["id1", "id2"], ["id3", "id4"], ["id5", "id6"]]
def get_job_requisition_id_batches(filter):
    job_requisitions_count = get_job_requisitions_count(filter)

    pages = math.ceil(job_requisitions_count / DEFAULT_QUERY_PAGINATION_SIZE)

    logger.info(f"Total job requisitions count: {job_requisitions_count}")
    job_requisition_ids_batches = []

    for page in range(pages):
        logger.info(f"Getting job requisition ids for page {page}")
        job_requisition_ids = get_job_requisition_ids_with_pagination(filter, page)
        job_requisition_ids_batches.append(job_requisition_ids)

    return job_requisition_ids_batches
