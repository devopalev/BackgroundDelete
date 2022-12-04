import logging
import os

logger = logging.getLogger(__name__)

# ### Settings ### #
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")  # Your bot token
URL_DELETE_BACKGROUND = "http://" + os.getenv("EDIT_IMAGES_HOST") + ":8080" + "/delete_background"  # microservice
COUNT_LIMIT_HANDLER_PHOTO = 10  # photo
TIME_LIMIT_HANDLER_PHOTO = 300  # second

# Use system (Read Only)
SYS_USER_PERSISTENT_KEY = "USER_DATA"
STATISTICS_FILE_NAME = "statistics.json"

