import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로딩 (cp949 인코딩)
@st.cache_data
def load_data():
    df = pd.read_csv("202506_202506_연령별인구현황_월간.csv", encoding="cp949")
    return df

df = load_data()

# 연령별 컬럼 목록 추출
age_columns = [col for col in df.columns if "세" in col]

# 행정구역 목록에서 중복 제거 후 정렬
region_options = df["행정구역"].unique()
region_selected = st.selectbox("지역을 선택하세요:", region_options)

# 선택된 지역의 데이터 가져오기
region_data = df[df["행정구역"] == region_selected].iloc[0]
raw_age_data = region_data[age_columns]

# 문자열 → 숫자 변환 (콤마 제거)
age_data = raw_age_data.apply(lambda x: int(str(x).replace(",", "")))

# 연령 추출 (100세 이상 포함)
ages = [
    int(col.split("_")[2].replace("세", "").replace("이상", ""))
    if "이상" not in col else 100
    for col in age_columns
]

# 시각화용 데이터프레임 구성
age_df = pd.DataFrame({
    "연령": ages,
    "인구수": age_data.values
})

# Plotly 그래프 생성
fig = px.bar(
    age_df,
    x="연령",
    y="인구수",
    labels={"연령": "나이", "인구수": "인구 수"},
    title=f"{region_selected} 연령별 인구 분포 (2025년 6월)",
    template="plotly_white"
)

# Streamlit 출력
st.title("지역별 연령별 인구 시각화")
st.plotly_chart(fig)
