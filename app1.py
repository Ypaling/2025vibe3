import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 연령별 인구 분석 (2025년 6월 기준)")

uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (합계 or 남녀)", type=["csv"])

def clean_and_convert(df, columns):
    for col in columns:
        df[col] = df[col].astype(str).str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    return df

def process_total_format(df):
    """정상 열 구조 처리"""
    seoul_df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()
    colnames = list(seoul_df.columns)
    age_cols = [c for c in colnames if "계_" in c and "세" in c]
    seoul_df = clean_and_convert(seoul_df, age_cols)

    total_counts = seoul_df[age_cols].sum().reset_index()
    total_counts.columns = ['연령', '전체']
    total_counts['연령'] = total_counts['연령'].str.extract(r'(\d+세|100세 이상)').squeeze()
    total_counts = total_counts.dropna()

    return total_counts

def process_transposed_format(df):
    """전치된 구조 처리"""
    df_transposed = df.T.reset_index()
    df_transposed.columns = df_transposed.iloc[0]  # 첫 행을 헤더로
    df_transposed = df_transposed[1:]

    # 서울시 전체 열 찾기
    if "서울특별시  (1100000000)" in df_transposed.columns:
        total_col = "서울특별시  (1100000000)"
    else:
        total_col = df_transposed.columns[1]

    df_transposed["연령"] = df_transposed.iloc[:, 0]
    df_transposed["전체"] = df_transposed[total_col].astype(str).str.replace(",", "").str.strip()
    df_transposed["전체"] = pd.to_numeric(df_transposed["전체"], errors='coerce').fillna(0).astype(int)
    df_transposed["연령"] = df_transposed["연령"].str.extract(r'(\d+세|100세 이상)').squeeze()
    df_transposed = df_transposed.dropna(subset=["연령"])

    return df_transposed[["연령", "전체"]]

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 구조 판별: 전치형이면 index에 "2025년06월_계_0세" 같은 값이 있음
    if "2025년06월_계_0세" in df.iloc[:, 0].values:
        st.info("🔄 전치된 형태의 CSV 감지됨 → 자동 변환 중...")
        total_df = process_transposed_format(df)
    else:
        st.info("✅ 표준 열 기반 CSV 감지됨 → 분석 중...")
        total_df = process_total_format(df)

    # 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=total_df['연령'], y=total_df['전체'], mode='lines+markers', name='전체'))
    fig.update_layout(title='서울특별시 연령별 전체 인구수', xaxis_title='연령', yaxis_title='인구수', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    # TOP 5
    top5 = total_df.sort_values(by="전체", ascending=False).head(5)
    st.subheader("👑 인구수가 많은 연령 TOP 5")
    st.table(top5.reset_index(drop=True))
else:
    st.info("CSV 파일을 업로드해주세요.")
