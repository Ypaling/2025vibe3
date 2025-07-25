import streamlit as st
import pandas as pd

st.set_page_config(page_title="남녀 인구 데이터 처리기", page_icon="📊")
st.title("👫 남녀 인구 데이터 업로드 및 합계 계산")

uploaded_file = st.file_uploader("📂 엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        st.subheader("원본 데이터 미리보기")
        st.dataframe(df.head())

        # '남'과 '여' 열이 있는지 확인
        if '남' in df.columns and '여' in df.columns:
            # 숫자로 변환 + NaN → 0 처리 + 정수로 변환
            for col in ['남', '여']:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            # 합계 계산
            df['합계'] = df['남'] + df['여']

            st.subheader("✅ 처리된 데이터")
            st.dataframe(df)

            # 다운로드 기능 (선택 사항)
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 CSV 다운로드",
                data=csv,
                file_name='남녀_인구_합계.csv',
                mime='text/csv',
            )
        else:
            st.warning("⚠️ '남' 또는 '여' 열이 존재하지 않습니다. 엑셀 열 이름을 확인해주세요.")

    except Exception as e:
        st.error(f"❌ 파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("좌측에서 엑셀 파일을 업로드해주세요.")
