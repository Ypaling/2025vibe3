import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", page_icon="📈", layout="wide")
st.title("📈 서울특별시 연령별 인구 분석 (2025년 6월 기준)")

uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (남녀구분 or 합계)", type=["csv"])

def clean_and_convert(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0).astype(int)
    return df

def analyze_gender_file(df):
    st.success("✅ 남녀구분 파일 인식됨")

    df_seoul = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()
    male_cols = [col for col in df_seoul.columns if "남_" in col and "세" in col]
    female_cols = [col for col in df_seoul.columns if "여_" in col and "세" in col]

    df_seoul = clean_and_convert(df_seoul, male_cols + female_cols)

    male = df_seoul[male_cols].sum().reset_index()
    female = df_seoul[female_cols].sum().reset_index()
    male.columns = ['연령', '남자']
    female.columns = ['연령', '여자']

    male['연령'] = male['연령'].str.extract(r'(\d+세|100세 이상)')
    female['연령'] = female['연령'].str.extract(r'(\d+세|100세 이상)')

    df_age = pd.merge(male, female, on='연령')
    df_age["전체"] = df_age["남자"] + df_age["여자"]

    # 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_age["연령"], y=df_age["남자"], mode='lines+markers', name='👦 남자', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df_age["연령"], y=df_age["여자"], mode='lines+markers', name='👧 여자', line=dict(color='red')))
    fig.update_layout(title="연령별 남녀 인구수", xaxis_title="연령", yaxis_title="인구수", hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("👑 인구 많은 연령 TOP 5")
    st.table(df_age.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))

def analyze_total_file(df):
    st.success("✅ 합계 파일 (전치형 구조) 인식됨")

    # 전치 구조 처리
    df_t = df.set_index(df.columns[0]).T.reset_index()
    df_t.columns.name = None

    total_col = "서울특별시  (1100000000)"
    if total_col not in df_t.columns:
        st.error(f"❌ '{total_col}' 열이 존재하지 않습니다. 실제 열 이름을 확인해주세요.")
        st.write("사용 가능한 열 목록:", list(df_t.columns))
        return

    df_t["연령"] = df_t.iloc[:, 0]
    df_t["전체"] = pd.to_numeric(df_t[total_col].astype(str).str.replace(",", "").str.strip(), errors="coerce").fillna(0).astype(int)
    df_t["연령"] = df_t["연령"].str.extract(r'(\d+세|100세 이상)')
    df_t = df_t.dropna(subset=["연령"])

    if df_t["전체"].sum() == 0:
        st.error("❗ 유효한 숫자 데이터가 없습니다. 숫자 변환 실패 가능성이 있습니다.")
        return

    # 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_t["연령"], y=df_t["전체"], mode='lines+markers', name='👥 전체', line=dict(color='green')))
    fig.update_layout(title="연령별 전체 인구수", xaxis_title="연령", yaxis_title="인구수", hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("👑 인구 많은 연령 TOP 5")
    st.table(df_t.sort_values(by="전체", ascending=False).head(5).reset_index(drop=True))

# 📂 파일 업로드 처리
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 구조 감지 및 분석 분기
    if any("남_" in col for col in df.columns) and any("여_" in col for col in df.columns):
        analyze_gender_file(df)
    elif df.columns[0].startswith("행정구역") and "2025년06월_계_0세" in df.iloc[:, 0].values:
        analyze_total_file(df)
    else:
        st.error("❗ 인식할 수 없는 형식입니다. 남녀구분 파일 또는 합계 전치 파일만 지원됩니다.")
else:
    st.info("CSV 파일을 업로드해주세요.")
