from utils.db_util import client
import requests
from utils.logger_util import logger


def get_job_requisition_ids():
    db = client["live-interview"]
    collection = db["jobRequisitions"]
    job_requisition_ids = collection.find(
        {"numberOfCancelledCandidates": 50}, {"_id": 1}
    )
    return [
        str(job_requisition_id["_id"]) for job_requisition_id in job_requisition_ids
    ]


def update_job_requisition(job_requisition_id):
    url = "http://host.docker.internal:3000/api/update-job-requisition"
    payload = {"jobRequisitionId": job_requisition_id}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info(f"Successfully updated job requisition {job_requisition_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update job requisition {job_requisition_id}: {str(e)}")


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
        },
    )
    result = res.json()

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
