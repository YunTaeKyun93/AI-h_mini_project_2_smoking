import os
from dotenv import load_dotenv

# 현재 settings.py 기준으로 상위 폴더에 .env 파일을 두고 읽는 구조
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# env 파일 로드
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

# ---------------------------------------------------------
# 📌 공통 설정
# ---------------------------------------------------------
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "50000"))

# ---------------------------------------------------------
# 📌 MySQL 설정 
# ---------------------------------------------------------
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "db": os.getenv("MYSQL_DB"),
    "charset": "utf8mb4",
}

# ---------------------------------------------------------
# 📌 MongoDB 설정
# ---------------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# ---------------------------------------------------------
# 📌 DB 선택 옵션
# ---------------------------------------------------------
USE_MYSQL = os.getenv("USE_MYSQL", "false").lower() == "true"
USE_MONGO = os.getenv("USE_MONGO", "false").lower() == "true"
