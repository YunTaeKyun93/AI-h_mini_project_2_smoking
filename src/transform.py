import pandas as pd
import numpy as np

from config.settings import PROCESSED_DATA_PATH

def transform_data(df: pd.DataFrame) -> pd.DataFrame:

    # 컬럼 매핑 (이후 템플릿 업데이트 요소 중 하나입니다 좀 불편)


    COLUMN_MAP = {
     
        "나이": "age",
        "키(cm)": "height",
        "몸무게(kg)": "weight",
        "BMI": "BMI",
        "시력": "sight",
        "충치": "cavity",
        "공복 혈당": "FPG",
        "혈압": "blood_pressure",
        "중성 지방": "TG",
        "혈청 크레아티닌": "SCR",
        "콜레스테롤": "cholesterol",
        "고밀도지단백": "HDL",
        "저밀도지단백": "LDL",
        "헤모글로빈": "Hb",
        "요 단백": "PRO",
        "간 효소율": "LFT",
        "label": "label",
        "ID": "id",
    }
    
    df = df.rename(columns=COLUMN_MAP)


    #  ID 정제 빈공간없애버리기 ~
 
    df["id"] = df["id"].astype(str).str.strip()
    df = df[df["id"] != ""]

  
    #  키 & 몸무게 처리 + BMI 재계산
    df["height"] = df["height"].replace(0, np.nan)
    df["weight"] = df["weight"].replace(0, np.nan)

    # 이걸 넣을까 말까 햇는데 bmi를 새로 계산 하다보니 없으면 중간값 보다는 그냥 없애는 게 맞다고 판단 height 또는 weight가 없으면 제거 
    df = df.dropna(subset=["height", "weight"])

    df["BMI"] = df["weight"] / (df["height"]/100)**2

    #  0 ==> NaN 변환해야 할 컬럼
    zero_to_nan = [
        "sight", "FPG", "blood_pressure", "TG", "SCR", 
        "cholesterol", "Hb", "HDL", "LDL", "LFT"
    ]

    for col in zero_to_nan:
        df[col] = df[col].replace(0, np.nan)

    df[zero_to_nan] = df[zero_to_nan].fillna(df[zero_to_nan].median())


    # 5) cavity (0/1 칼럼으로 정리)

    df["cavity"] = pd.to_numeric(df["cavity"], errors="coerce").fillna(0)
    df["cavity"] = df["cavity"].clip(0, 1).astype(int)


    #  label 정제

    df = df[df["label"].isin([0, 1])]
    df["label"] = df["label"].astype(int)

    return df

#  이후 업데이트 방안  :  컬럼 목록 및 비교 하는거 만들고, 기본적으로 사용되는 id값 정제 고정, 0=>nan 으로 교체 할거를 컬럼 명을 배열로 넣으면 가능하게 
# 그리고 범위형데이터도 몇개 모아서 한번에 하는게 편해보임 
def save_processed(df: pd.DataFrame):
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"📁 Transform 완료 — 파일 저장: {PROCESSED_DATA_PATH}")



#MI기법 검색하고 적용 해보기  