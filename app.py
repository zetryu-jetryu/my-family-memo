import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import urllib.parse

# 앱 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# --- 설정 구간 ---
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o" 
# 한글 인코딩 문제를 피하기 위해 주소를 안전하게 변환합니다.
base_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
URL = urllib.parse.quote(base_url, safe=':/?&=')
# ----------------

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # 데이터를 읽어올 때 캐시를 무효화하여 실시간성을 높입니다.
    return conn.read(spreadsheet=URL, ttl=0)

# 입력 섹션
with st.expander("📝 새 메모 남기기", expanded=True):
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["📅 일정", "🛒 장보기", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")

    if st.button("저장하기"):
        if content:
            try:
                # 1. 기존 데이터 로드
                df = load_data()
                
                # 2. 새 데이터 생성
                new_row = pd.DataFrame([{
                    "날짜": datetime.datetime.now().strftime("%m/%d %H:%M"),
                    "작성자": user,
                    "카테고리": category,
                    "내용": content
                }])
                
                # 3. 데이터 합치기
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # 4. 저장 (한글 포함 데이터 안전하게 전송)
                conn.update(spreadsheet=URL, data=updated_df)
                
                st.success("성공적으로 저장되었습니다!")
                st.rerun()
            except Exception as e:
                st.error(f"저장 중 오류가 발생했습니다: {e}")

# 메모 리스트 출력
st.divider()
try:
    display_df = load_data()
    if not display_df.empty:
        # 최신순 정렬 및 빈 줄 방지
        for i, row in display_df.iloc[::-1].iterrows():
            if pd.notna(row['내용']) and str(row['내용']).strip() != "":
                st.info(f"**[{row['entry.1933165763']}] {row['entry.1127160445']}** \n({row['entry.2016517978']} | {row['entry.1748127579']})")
except:
    st.write("아직 등록된 메모가 없습니다.")

