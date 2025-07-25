import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 설정
# -------------------------------
st.set_page_config(page_title="서울시 연령별 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 전체 인구의 연령별 분포")

# -------------------------------
# 업로드된 파일 경로
# -------------------------------
FILE_PATH = "/mnt/data/202506_202506_연령별인구현황_월간.csv"

@st.cache_data
def load_and_process_data():
    df = pd.read_csv(FILE_PATH, encoding="cp949")

    # '서울특별시' 전체 행 추출
    df_total = df[df["행정구역"].str.contains("서울특별시") & ~df["행정구역"].str.contains("구")]
    
    # 연령별 인구 컬럼만 추출
    age_cols = [col for col in df_total.columns if "세" in col]
    
    # 연령 라벨 추출 (0세 ~ 100세 이상)
    ages = [col.split("_")[-1] for col in age_cols]
    
    # 인구수 추출 및 숫자로 변환
    pop_values = df_total[age_cols].iloc[0].astype(str).str.replace(",", "").astype(int)
    
    df_age = pd.DataFrame({
        "연령": ages,
        "인구수": pop_values
    })
    
    return df_age

# -------------------------------
# 데이터 로드
# -------------------------------
df_age = load_and_process_data()

# -------------------------------
# 시각화
# -------------------------------
st.subheader("🧑‍🤝‍🧑 연령대별 인구 수 (2025년 6월 기준)")

fig = px.bar(
    df_age,
    x="연령",
    y="인구수",
    color_discrete_sequence=["darkblue"],
    labels={"연령": "연령", "인구수": "인구 수"},
    height=550
)

fig.update_layout(
    xaxis_tickangle=-60,
    bargap=0.15
)

st.plotly_chart(fig, use_container_width=True)
