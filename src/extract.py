import pandas as pd
from config.settings import CHUNK_SIZE
from src.utils import log

def extract_csv(file_path):
    log(f"📥 Extract 시작 — 파일: {file_path}")

    try:
        chunks = pd.read_csv(file_path, chunksize=CHUNK_SIZE)
        log(f"CSV 파일을 {CHUNK_SIZE} 행 단위로 로딩합니다.")
        return chunks
    except Exception as e:
        log(f"❌ Extract 오류: {e}")
        raise
