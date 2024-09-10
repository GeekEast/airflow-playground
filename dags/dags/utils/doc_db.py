import pymongo

from utils.variable_util import get_variable

# reuse db client
client = None


def get_docdb_connection(db_name):
    mongo_v3_host = get_variable("MONGO_V3_HOST")
    mongo_v3_user = get_variable("MONGO_V3_USER")
    mongo_v3_pass = get_variable("MONGO_V3_PASS")

    global client
    if client is None:
        client = pymongo.MongoClient(
            mongo_v3_host,
            username=mongo_v3_user,
            password=mongo_v3_pass,
            authSource=db_name,
            retryWrites=False,  # * very important to add retryWrites=False since DocumentDB doesn't support it.
        )

    conn = client[db_name]
    return client, conn