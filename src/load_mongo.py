from pymongo import MongoClient, ASCENDING
from src.utils import log
from config.settings import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION


def load_to_mongo(df):
    log("📦 MongoDB 등록 시작")

    if not MONGO_URI or not MONGO_DB_NAME or not MONGO_COLLECTION:
        raise ValueError("❌ MongoDB 설정이 올바르지 않습니다. .env 파일을 확인하세요.")

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]  
    collection = db[MONGO_COLLECTION]


    data = df.to_dict("records")

    try:
        # Insert
        result = collection.insert_many(data)
        log(f"✅ MongoDB Insert 완료 — {len(result.inserted_ids)}건 삽입")

        if "timestamp" in df.columns:
            collection.create_index([("timestamp", ASCENDING)])
            log("📌 Index 생성 완료: timestamp ASC")

    except Exception as e:
        log(f"❌ MongoDB Load 오류: {e}")

    finally:
        client.close()
        log("🔌 MongoDB 연결 종료")
