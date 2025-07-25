import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(page_title="서울시 연령별 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 전체 인구의 연령별 분포")

# -------------------------------
# 파일 경로 (업로드된 경로 직접 사용)
# -------------------------------
FILE_PATH = "/mnt/data/202506_202506_연령별인구현황_월간 합계.csv"

@st.cache_data
def load_data():
    # CSV 불러오기
    df = pd.read_csv(FILE_PATH, encoding="cp949")

    # 서울특별시 전체 인구만 사용 (첫 번째 행)
    df_seoul = df.iloc[0]

    # 연령별 컬럼만 필터링
    age_cols = [col for col in df_seoul.index if "세" in col and "계" in col]
    ages = [col.split("_")[-1] for col in age_cols]
    
    # 숫자 변환
    values = df_seoul[age_cols].astype(str).str.replace(",", "").astype(int)

    df_age = pd.DataFrame({
        "연령": ages,
        "인구수": values
    })

    return df_age

# -------------------------------
# 데이터 불러오기
# -------------------------------
df_age = load_data()

# -------------------------------
# 시각화
# -------------------------------
st.subheader("📈 연령별 인구 분포 (2025년 6월 기준)")

fig = px.bar(
    df_age,
    x="연령",
    y="인구수",
    color_discrete_sequence=["indigo"],
    labels={"연령": "연령", "인구수": "인구 수"},
    height=500
)

fig.update_layout(
    xaxis_tickangle=-60,
    bargap=0.1
)

st.plotly_chart(fig, use_container_width=True)
