from utils.variable_util import get_variable


STAGE = get_variable("STAGE")
REGION = get_variable("REGION")
REGION_SHORT = get_variable("REGION_SHORT")


IS_LOCAL = STAGE == "local" or STAGE is None or STAGE == ""
IS_TEST = STAGE == "test"
IS_DEV = STAGE == "dev"
IS_OFFLINE = IS_LOCAL or IS_TEST or IS_DEV

# we don't have airflow running in dev environment
IS_QA = STAGE == "qa"
IS_SANDBOX = STAGE == "sandbox"
IS_PRODUCT = STAGE == "product"
IS_ONLINE = IS_QA or IS_SANDBOX or IS_PRODUCT


# ph internal service call header secret
PH_INTERNAL_SERVICE_SECRET = get_variable("PH_INTERNAL_SERVICE_SECRET")

# ph internal server to server call token
PH_INTERNAL_SERVER_TO_SERVER_TOKEN = get_variable("PH_INTERNAL_SERVER_TO_SERVER_TOKEN")

# core-li endpoint
LI_CORE_GRAPHQL_ENDPOINT = f"https://ph-phapi-core-li-internal.{REGION}.{STAGE}.predictivehire.com/api/{REGION}/graphql"

MONGO_APPS_V3_DBNAME = get_variable("MONGO_APPS_V3_DBNAME")
MONGO_LI_V3_DBNAME = get_variable("MONGO_LI_V3_DBNAME")

# database default query pagination size
DEFAULT_QUERY_PAGINATION_SIZE = 100
