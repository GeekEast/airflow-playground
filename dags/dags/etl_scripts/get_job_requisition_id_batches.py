from bson import ObjectId


def get_job_requisition_id_batches():
    # job_requisition_ids = get_job_requisition_ids()
    job_requisition_ids = [str(ObjectId()) for _ in range(1000)]

    return [
        job_requisition_ids[i : i + 100]
        # page size 100
        for i in range(0, len(job_requisition_ids), 100)
    ]
