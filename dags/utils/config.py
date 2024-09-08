"""
Store all configs here
"""

from utils.logger_util import logger
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

# temporary files
TMP_BUCKET_SHORT_NAME = "ph-airflow2-tmpfile-bucket"
TMP_BUCKET_FULL_NAME = f"{STAGE}-{REGION_SHORT}-{TMP_BUCKET_SHORT_NAME}"

# ph internal service call header secret
PH_INTERNAL_SERVICE_SECRET = get_variable("PH_INTERNAL_SERVICE_SECRET")

# ph internal server to server call token
PH_INTERNAL_SERVER_TO_SERVER_TOKEN = get_variable("PH_INTERNAL_SERVER_TO_SERVER_TOKEN")

# core-li endpoint
LI_CORE_GRAPHQL_ENDPOINT = f"https://ph-phapi-core-li-internal.{REGION}.{STAGE}.predictivehire.com/api/{REGION}/graphql"

# core-apps graphql endpoint
APPS_CORE_GRAPHQL_ENDPOINT = f"https://ph-phapi-apps-core.{REGION}.{STAGE}.predictivehire.com/api/{REGION}/graphql"

IDP_BCRYPT_4ROUND_SALT = get_variable("IDP_BCRYPT_4ROUND_SALT")

MONGO_APPS_V3_DBNAME = get_variable("MONGO_APPS_V3_DBNAME")

MONGO_LI_V3_DBNAME = get_variable("MONGO_LI_V3_DBNAME")

# database default query pagination size
DEFAULT_QUERY_PAGINATION_SIZE = 100

# ------------------------------------
logger.info(
    "################################################################################"
)
logger.info("Configurations for eng/general dags: ")
logger.info(f"STAGE={STAGE}")
logger.info(f"REGION={REGION}")
logger.info(f"REGION_SHORT={REGION_SHORT}")
logger.info(f"APPS_CORE_GRAPHQL_ENDPOINT={APPS_CORE_GRAPHQL_ENDPOINT}")
logger.info(f"CORE_LI_GRAPHQL_ENDPOINT={LI_CORE_GRAPHQL_ENDPOINT}")
logger.info(f"TMP_BUCKET_FULL_NAME={TMP_BUCKET_FULL_NAME}")
logger.info(
    "################################################################################"
)
