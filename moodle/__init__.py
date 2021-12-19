import logging, sys
from moodle.config import loginData as config

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)
if sys.version_info[0] < 3:
    log.error("You must need atleast python version > 3.x")
    sys.exit(1)

HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
WARNING = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
SERVER = config.server
if SERVER:
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()
    TOTAL_COURSE = int(getenv("TOTAL_COURSE"))
    START_TIME = getenv("START_TIME")
    END_TIME = getenv("END_TIME")
    USERNAME = getenv("USERNAME")
    PASSWORD = getenv("PASSWORD")
    SEMID = getenv("SEMID")
    TOKEN = getenv("TOKEN")
    CHAT_ID = getenv("CHAT_ID")
else:
    TOTAL_COURSE = config.totalcourse
    START_TIME = config.startTime
    END_TIME = config.endTime
    USERNAME = config.username
    PASSWORD = config.password
    SEMID = config.moodleSemId
    TOKEN = config.telgramtoken
    CHAT_ID = config.chatid
