import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석 디버그", page_icon="🛠️", layout="wide")
st.title("🛠️ 서울시 연령별 인구 분석 (디버깅 모드)")

uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (합계 or 남녀구분)", type=["csv"])

def clean_and_convert(df, columns):
    for col in columns:
        df[col] = df[col].astype(str).str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    return df

def process_total_format(df):
    st.subheader("🔎 [디버그] 원본 CSV 상위 미리보기")
    st.write(df.head())

    seoul_df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()
    colnames = list(seoul_df.columns)
    age_cols = [c for c in colnames if "계_" in c and "세" in c]

    st.subheader("📋 [디버그] 연령 컬럼 목록")
    st.write(age_cols[:10])  # 앞 10개만 보기

    st.subheader("🔧 [디버그] 숫자 변환 전 상위 데이터")
    st.write(seoul_df[age_cols].head())

    # 숫자 변환 시도
    seoul_df = clean_and_convert(seoul_df, age_cols)

    st.subheader("✅ [디버그] 숫자로 변환된 합계 데이터 (0이면 실패)")
    st.write(seoul_df[age_cols].sum())

    # 최종 변환
    total_counts = seoul_df[age_cols].sum().reset_index()
    total_counts.columns = ['연령', '전체']
    total_counts['연령'] = total_counts['연령'].str.extract(r'(\d+세|100세 이상)').squeeze()
    total_counts = total_counts.dropna()

    return total_counts

def process_transposed_format(df):
    st.info("🔄 전치된 구조로 판단됨 → 자동 전치 처리 중...")
    df_transposed = df.T.reset_index()
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed[1:]

    if "서울특별시  (1100000000)" in df_transposed.columns:
        total_col = "서울특별시  (1100000000)"
    else:
        total_col = df_transposed.columns[1]

    df_transposed["연령"] = df_transposed.iloc[:, 0]
    df_transposed["전체"] = df_transposed[total_col].astype(str).str.replace(",", "").str.strip()
    df_transposed["전체"] = pd.to_numeric(df_transposed["전체"], errors="coerce").fillna(0).astype(int)
    df_transposed["연령"] = df_transposed["연령"].str.extract(r'(\d+세|100세 이상)').squeeze()
    df_transposed = df_transposed.dropna(subset=["연령"])

    st.subheader("✅ [디버그] 전치된 구조에서 추출한 데이터")
    st.write(df_transposed.head())

    return df_transposed[["연령", "전체"]]

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 전치형 구조 여부 판단
    if "2025년06월_계_0세" in df.iloc[:, 0].values:
        total_df = process_transposed_format(df)
    else:
        total_df = process_total_format(df)

    if not total_df.empty and total_df["전체"].sum() > 0:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=total_df['연령'], y=total_df['전체'],
                                 mode='lines+markers', name='전체'))
        fig.update_layout(title='서울특별시 연령별 전체 인구수',
                          xaxis_title='연령', yaxis_title='인구수', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("👑 인구 많은 연령 TOP 5")
        top5 = total_df.sort_values(by="전체", ascending=False).head(5)
        st.table(top5.reset_index(drop=True))
    else:
        st.error("❗ 유효한 데이터가 없습니다. 숫자 변환 실패 가능성 있음. 위 디버그 출력을 확인하세요.")
else:
    st.info("CSV 파일을 업로드해주세요.")
