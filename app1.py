import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", page_icon="📊", layout="wide")
st.title("📊 서울시 연령별 인구 분석 (2025년 6월 기준)")

uploaded_file = st.file_uploader("📁 CSV 파일 업로드 (남녀구분 or 합계)", type=["csv"])

def clean_columns(df, columns):
    df = df.copy()
    for col in columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "").str.strip(), errors='coerce').fillna(0).astype(int)
    return df

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    seoul_df = df[df["행정구역"].str.contains("서울특별시 ") & ~df["행정구역"].str.contains("\(")].copy()
    colnames = list(seoul_df.columns)

    is_gender = any("남_" in col for col in colnames) and any("여_" in col for col in colnames)
    is_total = any("계_" in col for col in colnames)

    if is_gender:
        st.subheader("✅ 남녀구분 인구 데이터 분석")

        age_columns_male = [col for col in colnames if "남_" in col and "세" in col]
        age_columns_female = [col for col in colnames if "여_" in col and "세" in col]

        seoul_df = clean_columns(seoul_df, age_columns_male + age_columns_female)

        male_counts = seoul_df[age_columns_male].sum().reset_index()
        female_counts = seoul_df[age_columns_female].sum().reset_index()

        male_counts.columns = ['연령', '남자']
        female_counts.columns = ['연령', '여자']
        male_counts['연령'] = male_counts['연령'].str.extract(r'(\d+세|100세 이상)').squeeze()
        female_counts['연령'] = female_counts['연령'].str.extract(r'(\d+세|100세 이상)').squeeze()

        age_df = pd.merge(male_counts, female_counts, on='연령')
        age_df = age_df.dropna()
        age_df['남자'] = age_df['남자'].astype(int)
        age_df['여자'] = age_df['여자'].astype(int)

        # 시각화
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=age_df['연령'], y=age_df['남자'], mode='lines+markers', name='남자'))
        fig.add_trace(go.Scatter(x=age_df['연령'], y=age_df['여자'], mode='lines+markers', name='여자'))
        fig.update_layout(title='연령별 남녀 인구수', xaxis_title='연령', yaxis_title='인구수', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        # TOP 5
        age_df["전체"] = age_df["남자"] + age_df["여자"]
        top5 = age_df.sort_values(by="전체", ascending=False).head(5)
        st.subheader("👑 인구수가 많은 연령 TOP 5")
        st.table(top5[['연령', '남자', '여자', '전체']].reset_index(drop=True))

    elif is_total:
        st.subheader("✅ 전체 인구 데이터 분석")

        age_columns_total = [col for col in colnames if "계_" in col and "세" in col]
        seoul_df = clean_columns(seoul_df, age_columns_total)

        total_counts = seoul_df[age_columns_total].sum().reset_index()
        total_counts.columns = ['연령', '전체']
        total_counts['연령'] = total_counts['연령'].str.extract(r'(\d+세|100세 이상)').squeeze()
        total_counts = total_counts.dropna()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=total_counts['연령'], y=total_counts['전체'], mode='lines+markers', name='전체'))
        fig.update_layout(title='연령별 전체 인구수', xaxis_title='연령', yaxis_title='인구수', hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        top5 = total_counts.sort_values(by="전체", ascending=False).head(5)
        st.subheader("👑 인구수가 많은 연령 TOP 5")
        st.table(top5.reset_index(drop=True))

    else:
        st.error("⚠️ 남녀 또는 전체 인구 형식이 아닙니다.")
else:
    st.info("CSV 파일을 업로드해주세요.")
