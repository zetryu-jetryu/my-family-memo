import streamlit as st
import pandas as pd
import datetime
import requests

# 1. 기본 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# 2. 설정 구간
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
FORM_URL = "https://docs.google.com/forms/d/1lUs7h2cj-LGv-0RZjPWrsCLMJmt2CTzh9kvyzV8nlV0/formResponse"

ENTRIES = {
    "date": "entry.1691386708",
    "user": "entry.1460592934",
    "cat": "entry.348705031",
    "text": "entry.1509172605"
}

# 3. 데이터 로드 함수
def load_data():
    try:
        # 캐시 방지를 위해 현재 시간 추가
        url = f"{READ_URL}&t={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# 4. 입력 UI (Form 없이 직접 배치하여 반응성 향상)
with st.container():
    st.subheader("📝 새 메모 남기기")
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "첫째", "둘째"])
    category = st.selectbox("카테고리", ["🛒 장보기", "📅 일정", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요", placeholder="여기에 내용을 써주세요")
    
    # 버튼을 누르면 즉시 실행
    if st.button("저장하기", use_container_width=True):
        if content:
            payload = {
                ENTRIES["date"]: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                ENTRIES["user"]: user,
                ENTRIES["cat"]: category,
                ENTRIES["text"]: content
            }
            with st.spinner('저장 중...'):
                try:
                    # 전송 시도
                    response = requests.post(FORM_URL, data=payload, timeout=10)
                    if response.ok:
                        st.success("✅ 저장되었습니다! 아래 목록을 확인하세요.")
                        # 새로고침 없이 데이터를 즉시 다시 읽어오기 위해 처리
                        st.cache_data.clear()
                    else:
                        st.error(f"❌ 전송 실패 (코드: {response.status_code})")
                except Exception as e:
                    st.error(f"❌ 연결 오류: {e}")
        else:
            st.warning("⚠️ 내용을 입력해주세요.")

# 5. 메모 목록 표시
st.write("---")
st.subheader("📌 최근 메모")
df = load_data()

if not df.empty:
    try:
        # 데이터가 있다면 최신 10개 표시
        for i, row in df.iloc[::-1].head(10).iterrows():
            # 안전하게 데이터 추출 (열 개수에 맞게 조정)
            text = row.iloc[-1] if len(row) >= 1 else ""
            cat = row.iloc[-2] if len(row) >= 2 else ""
            who = row.iloc[-3] if len(row) >= 3 else ""
            when = row.iloc[-4] if len(row) >= 4 else ""
            
            if pd.notna(text) and text != "":
                st.info(f"**[{cat}] {text}** \n({who} | {when})")
    except Exception as e:
        st.write("메모를 불러오는 중입니다...")
else:
    st.write("표시할 메모가 없습니다. 첫 메모를 남겨보세요!")
