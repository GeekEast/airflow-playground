from etl_scripts.apis.core_li import update_job_requisition


def task_backfill_number_of_cancelled_candidates_in_batch(job_requisition_ids):
    # update_job_requisition one by one
    for job_requisition_id in job_requisition_ids:
        update_job_requisition(job_requisition_id)
