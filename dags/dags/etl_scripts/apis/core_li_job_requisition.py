import requests

from dags.utils.doc_db import get_docdb_connection
from dags.etl_scripts.config import (
    DEFAULT_QUERY_PAGINATION_SIZE,
    LI_CORE_GRAPHQL_ENDPOINT,
    MONGO_LI_V3_DBNAME,
    PH_INTERNAL_SERVER_TO_SERVER_TOKEN,
    PH_INTERNAL_SERVICE_SECRET,
)
from utils.logger_util import logger


def get_job_requisitions_count(filter):
    docdb_conn = None
    li_db_name = MONGO_LI_V3_DBNAME

    try:
        docdb_client, docdb_conn = get_docdb_connection(li_db_name)
        collection = docdb_conn["jobRequisitions"]

        job_requisitions_total = collection.count_documents(filter)
        return job_requisitions_total
    except Exception as e:
        raise ValueError(e)


def get_job_requisition_ids_with_pagination(filter, page_number):
    docdb_conn = None
    li_db_name = MONGO_LI_V3_DBNAME

    try:
        docdb_client, docdb_conn = get_docdb_connection(li_db_name)
        collection = docdb_conn["jobRequisitions"]

        skip = page_number * DEFAULT_QUERY_PAGINATION_SIZE
        limit = DEFAULT_QUERY_PAGINATION_SIZE

        job_requisitions = collection.find(filter, {"_id": 1}).skip(skip).limit(limit)
        ids_str = [str(job_requisition["_id"]) for job_requisition in job_requisitions]
        return ids_str
    except Exception as e:
        raise ValueError(e)


def recalculate_job_requisition_status(job_requisition_id: str):
    query = """
        mutation LIRecalculateJobRequisitionStatus($filter: LIRecalculateJobRequisitionStatusDto!) {
            LIRecalculateJobRequisitionStatus(filter: $filter)
        }
    """

    mutation_variables = {
        "filter": {
            "jobRequisitionId": job_requisition_id,
        }
    }

    res = requests.post(
        LI_CORE_GRAPHQL_ENDPOINT,
        json={"query": query, "variables": mutation_variables},
        headers={
            "authorization": f"Bearer {PH_INTERNAL_SERVER_TO_SERVER_TOKEN}",
            "hire": PH_INTERNAL_SERVICE_SECRET,
            "content-type": "application/json",
        },
    )

    try:
        result = res.json()
    except Exception as e:
        logger.error(e)
        raise Exception(
            f"cannot parse the response from the recalculate job requisition status api - {res.text}"
        )

    if res.status_code == 200:
        if "errors" in result:
            error_message = result["errors"][0]["message"]
            raise Exception(
                f"recalculate job requisition status - {job_requisition_id} get an error which is {error_message}"
            )
        # the request is ok and there is no error
        else:
            logger.info(
                f"recalculate job requisition status - {job_requisition_id} SUCCESSFULLY!"
            )
    else:
        raise Exception(
            f"recalculate job requisition status failed - error code - {res.status_code} - the job requisition is {job_requisition_id}"
        )
