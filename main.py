from src.extract import extract_csv
from src.transform import transform_data
from src.load_mysql import load_to_mysql
from src.load_mongo import load_to_mongo
from config.settings import RAW_DATA_PATH
from src.utils import log
import questionary

def choose_db():
    choice = questionary.select(
        "📦 어떤 DB에 등록할까요?",
        choices=[
            "MySQL",
            "MongoDB",
            "MySQL + MongoDB",
            "취소"
        ]
    ).ask()
    return choice


def main():
    log("🚀 ETL 파이프라인 시작")

    option = choose_db()

    if option == "취소":
        log("프로그램을 종료합니다.")
        return

    log("📥 Extract 단계 시작")
    chunk_iterator = extract_csv(RAW_DATA_PATH)

    total_rows = 0

    for chunk in chunk_iterator:
        transformed_df = transform_data(chunk)
        rows = len(transformed_df)
        total_rows += rows

        log(f"🔧 변환된 Chunk 처리 중… ({rows} rows)")

        # Load
        if option == "MySQL":
            load_to_mysql(transformed_df)
            print(option)

        elif option == "MongoDB":
            load_to_mongo(transformed_df)
            print(option)

        elif option == "MySQL + MongoDB":
            load_to_mysql(transformed_df)
            load_to_mongo(transformed_df)
            print(option)

    log(f"🎉 ETL 전체 완료 — 총 {total_rows} rows 처리")


if __name__ == "__main__":
    main()
