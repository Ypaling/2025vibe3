import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="남녀 인구 데이터 처리기", page_icon="📊")
st.title("👫 남녀 인구 데이터 업로드 및 합계 계산")

uploaded_file = st.file_uploader("📂 엑셀 또는 CSV 파일을 업로드하세요", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        file_name = uploaded_file.name
        _, ext = os.path.splitext(file_name)

        # 파일 읽기
        if ext.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(uploaded_file)
        elif ext.lower() == ".csv":
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="cp949")
        else:
            st.error("지원하지 않는 파일 형식입니다.")
            st.stop()

        st.subheader("📄 원본 데이터 미리보기")
        st.dataframe(df.head())

        # '남', '여' 열 처리
        if '남' in df.columns and '여' in df.columns:
            for col in ['남', '여']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            df['합계'] = df['남'] + df['여']

            st.subheader("✅ 처리된 데이터")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv,
                file_name='남녀_인구_합계.csv',
                mime='text/csv',
            )
        else:
            st.warning("⚠️ '남' 또는 '여' 열이 존재하지 않습니다. 열 이름을 확인해주세요.")

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")
else:
    st.info("좌측에서 엑셀 또는 CSV 파일을 업로드해주세요.")
