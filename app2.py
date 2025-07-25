import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로딩 (cp949 인코딩)
@st.cache_data
def load_data():
    df = pd.read_csv("202506_202506_연령별인구현황_월간.csv", encoding="cp949")
    return df

df = load_data()

# 서울시 전체 데이터만 필터링
seoul_total = df[df['행정구역'].str.contains("서울특별시") & ~df['행정구역'].str.contains("구")].iloc[0]

# 연령별 인구 컬럼만 추출
age_columns = [col for col in df.columns if "세" in col]
raw_age_data = seoul_total[age_columns]

# 모든 값을 문자열로 변환 후 콤마 제거 및 정수 변환
age_data = raw_age_data.apply(lambda x: int(str(x).replace(",", "")))

# 나이값 추출
ages = [int(col.split("_")[2].replace("세", "").replace("이상", "")) if "이상" not in col else 100 for col in age_columns]

# 시각화용 데이터프레임 구성
age_df = pd.DataFrame({
    "연령": ages,
    "인구수": age_data.values
})

# Plotly Bar Chart
fig = px.bar(age_df, x="연령", y="인구수",
             labels={"연령": "나이", "인구수": "인구 수"},
             title="서울특별시 연령별 인구 분포 (2025년 6월)",
             template="plotly_white")

# Streamlit 출력
st.title("서울특별시 연령별 인구 시각화")
st.plotly_chart(fig)
