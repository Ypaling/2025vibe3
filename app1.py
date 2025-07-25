import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --------------------------
# 페이지 설정
# --------------------------
st.set_page_config(page_title="서울시 남녀 인구 분석", page_icon="👨‍👩‍👧‍👦", layout="wide")
st.title("👨‍👩‍👧‍👦 서울시 연령별 남녀 인구 분석")

# --------------------------
# 파일 경로
# --------------------------
file_gender = "202506_202506_연령별인구현황_월간_남녀구분.csv"

# --------------------------
# 데이터 불러오기 및 전처리
# --------------------------
@st.cache_data
def load_gender_data():
    df = pd.read_csv(file_gender, encoding="cp949")

    # 서울시 데이터만 필터링
    df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()

    # 남/여 컬럼 추출
    male_cols = [col for col in df.columns if "남_" in col and "세" in col]
    female_cols = [col for col in df.columns if "여_" in col and "세" in col]

    # 숫자 변환 (콤마 제거)
    for col in male_cols + female_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0)

    # 합계 계산
    male_sum = df[male_cols].sum().reset_index()
    female_sum = df[female_cols].sum().reset_index()
    male_sum.columns = ["연령", "남자"]
    female_sum.columns = ["연령", "여자"]

    # 연령 정리
    male_sum["연령"] = male_sum["연령"].str.extract(r'(\d+세|100세 이상)')
    female_sum["연령"] = female_sum["연령"].str.extract(r'(\d+세|100세 이상)')

    # 병합 후 전체 계산
    df_gender = pd.merge(male_sum, female_sum, on="연령")
    df_gender["전체"] = df_gender["남자"] + df_gender["여자"]

    return df_gender

# --------------------------
# 데이터 로드
# --------------------------
df_gender = load_gender_data()

# --------------------------
# 시각화
# --------------------------
st.header("📈 연령별 남녀 인구수 그래프")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_gender["연령"],
    y=df_gender["남자"],
    mode='lines+markers',
    name='👦 남자',
    line=dict(color='blue')
))
fig.add_trace(go.Scatter(
    x=df_gender["연령"],
    y=df_gender["여자"],
    mode='lines+markers',
    name='👧 여자',
    line=dict(color='red')
))
fig.update_layout(
    title="연령별 남녀 인구수 비교",
    xaxis_title="연령",
    yaxis_title="인구수",
    hovermode='x unified'
)
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# 상위 5개 연령대 표시
# --------------------------
st.subheader("🔝 남녀 전체 인구 기준 상위 5개 연령")
st.table(df_gender.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))
