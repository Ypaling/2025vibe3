import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(page_title="서울시 남녀 인구 시각화", page_icon="👫", layout="wide")
st.title("👫 서울시 남성과 여성 인구의 연령별 비교")

# --------------------------
# CSV 파일 경로
# --------------------------
file_path = "202506_202506_연령별인구현황_월간_남녀구분.csv"

@st.cache_data
def load_gender_data():
    # CSV 불러오기
    df = pd.read_csv(file_path, encoding="cp949")

    # 서울특별시 전체 데이터만 필터링
    df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()

    # 남자/여자 연령 컬럼 추출
    male_cols = [col for col in df.columns if "남_" in col and "세" in col]
    female_cols = [col for col in df.columns if "여_" in col and "세" in col]

    # 숫자 변환
    for col in male_cols + female_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0)

    # 연령별 합계
    male = df[male_cols].sum().reset_index()
    female = df[female_cols].sum().reset_index()
    male.columns = ["연령", "남성"]
    female.columns = ["연령", "여성"]

    # 연령 이름 정리
    male["연령"] = male["연령"].str.extract(r"남_(\d+세|100세 이상)")
    female["연령"] = female["연령"].str.extract(r"여_(\d+세|100세 이상)")

    # 병합
    merged = pd.merge(male, female, on="연령")
    return merged

# --------------------------
# 데이터 불러오기
# --------------------------
df = load_gender_data()

# --------------------------
# 시각화: 겹쳐진 막대 그래프
# --------------------------
fig = go.Figure()

# 남성
fig.add_trace(go.Bar(
    x=df["연령"],
    y=df["남성"],
    name="남성",
    marker_color='blue'
))

# 여성 (투명도 적용)
fig.add_trace(go.Bar(
    x=df["연령"],
    y=df["여성"],
    name="여성",
    marker_color='pink',
    opacity=0.6
))

fig.update_layout(
    barmode='overlay',
    title="서울시 남성과 여성 인구의 연령별 비교",
    xaxis_title="연령",
    yaxis_title="인구수",
    legend_title="성별",
    xaxis_tickangle=-60
)

st.plotly_chart(fig, use_container_width=True)

