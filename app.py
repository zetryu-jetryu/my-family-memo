import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 앱 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# --- 이 부분을 주의해서 수정하세요 ---
# 구글 시트 주소에서 'ID'만 따옴표 안에 넣으세요.
# 예: https://docs.google.com/spreadsheets/d/1abc123... 에서 1abc123 부분이 ID입니다.
SHEET_ID = "여기다가_복사한_ID만_넣으세요" 

# 한글 에러를 방지하기 위해 URL을 자동으로 생성하도록 만듭니다.
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
# ----------------------------------

conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 함수
def load_data():
    # 주소에 한글이 섞여 있을 경우를 대비해 인코딩 설정을 추가합니다.
    return conn.read(spreadsheet=URL, ttl=0)

# 입력 섹션
with st.expander("📝 새 메모 남기기", expanded=True):
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["📅 일정", "🛒 장보기", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")

    if st.button("저장하기"):
        if content:
            try:
                existing_data = load_data()
                new_data = pd.DataFrame([{
                    "날짜": datetime.datetime.now().strftime("%m/%d %H:%M"),
                    "작성자": user,
                    "카테고리": category,
                    "내용": content
                }])
                # 데이터 합치기 전 비어있는 행 제거
                updated_df = pd.concat([existing_data, new_data], ignore_index=True).dropna(how='all')
                
                # 저장 시도
                conn.update(spreadsheet=URL, data=updated_df)
                st.success("성공적으로 저장되었습니다!")
                st.rerun()
            except Exception as e:
                # 어떤 에러인지 화면에 구체적으로 표시합니다.
                st.error(f"오류 상세 내용: {e}")




