import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 연령별 남녀 인구 분석")

# CSV 경로
file_gender = "202506_202506_연령별인구현황_월간_남녀구분.csv"

@st.cache_data
def load_gender_data():
    df = pd.read_csv(file_gender, encoding="cp949")

    # 서울시 필터
    df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()

    # 열 이름에서 남자/여자 항목만 필터링
    male_cols = [col for col in df.columns if "_남_" in col and "세" in col]
    female_cols = [col for col in df.columns if "_여_" in col and "세" in col]

    # 숫자형으로 변환
    for col in male_cols + female_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0)

    # 남자/여자 합계
    male_sum = df[male_cols].sum().reset_index()
    female_sum = df[female_cols].sum().reset_index()

    # 연령 추출: 예시 → "2025년06월_남_45세" → "45세"
    male_sum["연령"] = male_sum["index"].str.extract(r'(\d+세|100세 이상)')
    female_sum["연령"] = female_sum["index"].str.extract(r'(\d+세|100세 이상)')
    male_sum = male_sum.rename(columns={0: "남자"})
    female_sum = female_sum.rename(columns={0: "여자"})

    # 병합
    df_gender = pd.merge(male_sum[["연령", "남자"]], female_sum[["연령", "여자"]], on="연령")
    df_gender["남자"] = pd.to_numeric(df_gender["남자"], errors="coerce").fillna(0)
    df_gender["여자"] = pd.to_numeric(df_gender["여자"], errors="coerce").fillna(0)
    df_gender["전체"] = df_gender["남자"] + df_gender["여자"]

    return df_gender

df_gender = load_gender_data()

# 그래프
st.header("📈 연령별 남녀 인구수 비교")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["남자"], mode="lines+markers", name="남자", line=dict(color="blue")))
fig.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["여자"], mode="lines+markers", name="여자", line=dict(color="red")))
fig.update_layout(title="연령별 남녀 인구수", xaxis_title="연령", yaxis_title="인구수", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# 상위 5개 연령
st.subheader("🔝 남녀 전체 인구 기준 상위 5개 연령")
st.table(df_gender.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))
