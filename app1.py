import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(page_title="서울시 인구 연령별 시각화", page_icon="📊", layout="wide")
st.title("📊 서울시 연령별 인구 시각화")

# --------------------------
# 데이터 불러오기 함수
# --------------------------
@st.cache_data
def load_total_data():
    df = pd.read_csv("202506_202506_연령별인구현황_월간_합계.csv", encoding="cp949")
    
    # 서울특별시 전체만 추출 (구/동 제외)
    df_seoul = df[df["행정구역"].str.contains("서울특별시  ") & ~df["행정구역"].str.contains("\(")]
    
    # 연령별 컬럼만 추출
    age_cols = [col for col in df_seoul.columns if "세" in col and "계" not in col]
    
    # 연령 추출
    ages = [col.split("_")[-1] for col in age_cols]
    
    # 인구수 추출
    population = df_seoul[age_cols].iloc[0].astype(str).str.replace(",", "").astype(int)
    
    # 데이터프레임 생성
    df_age = pd.DataFrame({
        "연령": ages,
        "인구수": population
    })

    return df_age

# --------------------------
# 데이터 로드
# --------------------------
df_age = load_total_data()

# --------------------------
# 시각화
# --------------------------
st.subheader("서울시 전체 인구의 연령별 분포")

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
