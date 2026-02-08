import streamlit as st
import pandas as pd
import datetime
import os

# 파일 기반 저장 (임시 방식 - 나중에 구글 시트로 업그레이드 권장)
DB_FILE = "family_memos.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["날짜", "작성자", "카테고리", "내용"])

# 페이지 설정
st.set_page_config(page_title="우리 가족 메모장", layout="centered")
st.title("🏠 우리 가족 공동 메모장")

# 입력 섹션
user = st.selectbox("누구신가요?", ["아빠", "엄마", "첫째", "둘째"])
category = st.selectbox("카테고리", ["🛒 장보기", "📅 일정", "💡 아이디어", "💬 기타"])
content = st.text_input("내용을 입력하세요")

if st.button("메모 추가"):
    if content:
        df = load_data()
        new_row = {
            "날짜": datetime.datetime.now().strftime("%m/%d %H:%M"),
            "작성자": user,
            "카테고리": category,
            "내용": content
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("저장되었습니다!")
        st.rerun()

# 저장된 메모 보기
st.divider()
df = load_data()
if not df.empty:
    for i, row in df.iloc[::-1].iterrows():
        st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
