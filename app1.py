import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(page_title="서울시 남녀 연령별 인구 분석", page_icon="🧑‍🤝‍🧑", layout="wide")
st.title("👨‍🦱👩 서울시 남성과 여성 인구의 연령별 비교")

# --------------------------
# CSV 파일 경로 (남녀 구분)
# --------------------------
file_path = "202506_202506_연령별인구현황_월간_남녀구분.csv"

@st.cache_data
def load_gender_data():
    df = pd.read_csv(file_path, encoding="cp949")
    
    # 서울시 전체 합계 행 추출 (구 단위, 동 단위 제외)
    df_total = df[df["행정구역"].str.contains("서울특별시  ") & ~df["행정구역"].str.contains("\(")]

    # 남성과 여성 열만 선택
    male_cols = [col for col in df_total.columns if "남_" in col and "세" in col]
    female_cols = [col for col in df_total.columns if "여_" in col and "세" in col]

    # 연령만 추출
    ages = [col.split("_")[-1] for col in male_cols]

    # 숫자로 변환
    male_values = df_total[male_cols].iloc[0].astype(str).str.replace(",", "").astype(int)
    female_values = df_total[female_cols].iloc[0].astype(str).str.replace(",", "").astype(int)

    # 데이터프레임 구성
    df_gender = pd.DataFrame({
        "연령": ages,
        "남성": male_values,
        "여성": female_values
    })

    return df_gender

# --------------------------
# 데이터 로드
# --------------------------
df_gender = load_gender_data()

# --------------------------
# 그래프 그리기
# --------------------------
fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_gender["연령"],
    y=df_gender["남성"],
    name="남성",
    marker_color="blue"
))

fig.add_trace(go.Bar(
    x=df_gender["연령"],
    y=df_gender["여성"],
    name="여성",
    marker_color="pink"
))

fig.update_layout(
    barmode="overlay",
    title="서울시 남성과 여성 인구의 연령별 비교",
    xaxis_title="연령",
    yaxis_title="인구",
    xaxis_tickangle=-60,
)

st.plotly_chart(fig, use_container_width=True)
