import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="서울시 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 연령별 인구 분석 결과 (자동 분석)")

# 파일 경로
file_total = "202506_202506_연령별인구현황_월간_합계.csv"
file_gender = "202506_202506_연령별인구현황_월간_남녀구분.csv"

# ------------------------------
# 데이터 불러오기 함수
# ------------------------------
@st.cache_data
def load_total_data():
    try:
        df = pd.read_csv(file_total, encoding="cp949")
    except:
        df = pd.read_csv(file_total, encoding="utf-8")
    df_t = df.set_index(df.columns[0]).T.reset_index()
    total_col = "서울특별시  (1100000000)"
    df_t["연령"] = df_t.iloc[:, 0]
    df_t["전체"] = pd.to_numeric(df_t[total_col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0).astype(int)
    df_t["연령"] = df_t["연령"].str.extract(r'(\d+세|100세 이상)')
    df_t = df_t.dropna(subset=["연령"])
    return df_t[["연령", "전체"]]

@st.cache_data
def load_gender_data():
    try:
        df = pd.read_csv(file_gender, encoding="cp949")
    except:
        df = pd.read_csv(file_gender, encoding="utf-8")
    df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()
    male_cols = [col for col in df.columns if "남_" in col and "세" in col]
    female_cols = [col for col in df.columns if "여_" in col and "세" in col]
    for col in male_cols + female_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0).astype(int)
    male = df[male_cols].sum().reset_index()
    female = df[female_cols].sum().reset_index()
    male.columns = ['연령', '남자']
    female.columns = ['연령', '여자']
    male["연령"] = male["연령"].str.extract(r'(\d+세|100세 이상)')
    female["연령"] = female["연령"].str.extract(r'(\d+세|100세 이상)')
    df_age = pd.merge(male, female, on="연령")
    df_age["전체"] = df_age["남자"] + df_age["여자"]
    return df_age

# ------------------------------
# 데이터 불러오기
# ------------------------------
df_total = load_total_data()
df_gender = load_gender_data()

# ------------------------------
# 전체 인구 그래프
# ------------------------------
st.header("👥 전체 연령별 인구수")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df_total["연령"], y=df_total["전체"], mode='lines+markers', name='전체', line=dict(color='green')))
fig1.update_layout(title="연령별 전체 인구수", xaxis_title="연령", yaxis_title="인구수", hovermode='x unified')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🔝 전체 인구 기준 상위 5개 연령")
st.table(df_total.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))

# ------------------------------
# 남녀 인구 그래프
# ------------------------------
st.header("👦👧 연령별 남녀 인구수 비교")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["남자"], mode='lines+markers', name='👦 남자', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=df_gender["연령"], y=df_gender["여자"], mode='lines+markers', name='👧 여자', line=dict(color='red')))
fig2.update_layout(title="연령별 남녀 인구수", xaxis_title="연령", yaxis_title="인구수", hovermode='x unified')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🔝 남녀 전체 인구 기준 상위 5개 연령")
st.table(df_gender.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))
