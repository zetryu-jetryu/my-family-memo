%%writefile app.py
import streamlit as st
import pandas as pd
import datetime
import os

# 파일 경로 (Colab 임시 폴더)
DB_FILE = "family_memos.csv"

# 데이터 로드 (파일이 없으면 새로 생성)
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["날짜", "작성자", "카테고리", "내용"])

st.set_page_config(page_title="가족 메모장", layout="centered")
st.title("🏠 우리 가족 공동 메모장")

# 입력 폼
user = st.selectbox("사용자 선택", ["아빠", "엄마", "첫째", "둘째"])
category = st.selectbox("카테고리", ["🛒 장보기", "📅 일정", "💡 아이디어", "💬 기타"])
content = st.text_input("내용을 입력하세요 (입력 후 '메모 추가' 클릭)")

if st.button("메모 추가"):
    if content.strip() != "":
        df = load_data()
        new_row = {
            "날짜": datetime.datetime.now().strftime("%m/%d %H:%M"),
            "작성자": user,
            "카테고리": category,
            "내용": content
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("✅ 메모가 저장되었습니다!")
        st.rerun() # 화면 새로고침
    else:
        st.warning("내용을 입력해 주세요.")

# 저장된 메모 보여주기
st.markdown("---")
df = load_data()
if not df.empty:
    for i, row in df.iloc[::-1].iterrows(): # 최신순
        st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
else:
    st.write("아직 등록된 메모가 없어요.")