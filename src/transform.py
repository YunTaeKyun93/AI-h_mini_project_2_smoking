import pandas as pd
import numpy as np
from src.utils import log
from config.settings import PROCESSED_DATA_PATH

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    log("🧹 Transform 시작")

    # 1. 컬럼명 통일
    df.columns = df.columns.str.lower()

    # 2. timestamp 변환 + timestamp 없는 행 제거
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # 3. activity 문자열 처리
    if "activity" in df.columns:
        df["activity"] = df["activity"].astype(str).str.strip()
        df["activity"] = df["activity"].replace("", "unknown")

    # 4. 생체 신호: 0 → 결측치 처리
    zero_as_missing = ["heart_rate", "blood_oxygen", "body_temp", "resp_rate"]
    for col in zero_as_missing:
        if col in df.columns:
            df[col] = df[col].replace(0, np.nan)

    # 5. step_count: NaN만 0으로
    if "step_count" in df.columns:
        df["step_count"] = df["step_count"].fillna(0)

    # 6. 센서데이터(accel/gyro): NaN은 median으로
    sensor_cols = ["accel_x", "accel_y", "accel_z",
                   "gyro_x", "gyro_y", "gyro_z"]
    for col in sensor_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # 7. is_tampered: 결측 0으로
    if "is_tampered" in df.columns:
        df["is_tampered"] = df["is_tampered"].fillna(0).astype(int)

    # 8. 모든 숫자형 컬럼의 남은 결측치를 median으로
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    return df


def save_processed(df: pd.DataFrame):
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    log(f"📁 Transform 완료 — 파일 저장: {PROCESSED_DATA_PATH}")
