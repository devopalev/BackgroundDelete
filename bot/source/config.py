import logging
import os

logger = logging.getLogger(__name__)

# ### Settings ### #
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")  # Your bot token
URL_DELETE_BACKGROUND = os.getenv("URL_MICROSERVICE_EDIT_IMAGES") + "/delete_background"  # URL microservice
COUNT_LIMIT_HANDLER_PHOTO = 10  # photo
TIME_LIMIT_HANDLER_PHOTO = 300  # second

# Use system (Read Only)
SYS_USER_PERSISTENT_KEY = "USER_DATA"
STATISTICS_FILE_PATH = "statistics.json"

