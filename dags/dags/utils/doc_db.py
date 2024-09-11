from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.operators.python import get_current_context
from utils.variable_util import get_variable
from utils.logger_util import logger


def get_docdb_connection(db_name):
    # get context from airflow
    ctx = get_current_context()
    region = ctx["params"]["region"]

    logger.info(f"Getting docdb connection for {db_name} in {region}")

    stage = get_variable("STAGE")
    mongo_conn_id = f"live-interview-{stage}-{region}"
    hook = MongoHook(mongo_conn_id=mongo_conn_id)
    client = hook.get_conn()
    db = client[db_name]

    return client, db
