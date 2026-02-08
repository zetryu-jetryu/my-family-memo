import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime

# 앱 설정
st.set_page_config(page_title="우리 가족 메모장", layout="centered")
st.title("🏠 우리 가족 공동 메모장")

# 구글 시트 연결 설정 (공개된 시트 주소 입력)
# 본인의 구글 시트 주소를 아래 따옴표 안에 넣어주세요.
URL = "https://docs.google.com/spreadsheets/d/본인의_시트_ID_입력/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

# 데이터 불러오기 함수
def load_data():
    return conn.read(spreadsheet=URL, usecols=[0,1,2,3])

# 입력 섹션
with st.container():
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["🛒 장보기", "📅 일정", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")

    if st.button("메모 추가"):
        if content:
            # 기존 데이터 가져오기
            existing_data = load_data()
            # 새 데이터 만들기
            new_data = pd.DataFrame([{
                "날짜": datetime.datetime.now().strftime("%m/%d %H:%M"),
                "작성자": user,
                "카테고리": category,
                "내용": content
            }])
            # 합치기
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            # 시트에 저장 (이 기능은 시트 공유가 '편집자'로 되어 있어야 함)
            conn.update(spreadsheet=URL, data=updated_df)
            st.success("메모가 시트에 저장되었습니다!")
            st.rerun()

# 메모 리스트 출력
st.divider()
try:
    df = load_data()
    if not df.empty:
        for i, row in df.iloc[::-1].iterrows(): # 최신순
            if pd.notna(row['내용']):
                st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
except:
    st.write("아직 등록된 메모가 없거나 시트 연결 확인이 필요합니다.")
