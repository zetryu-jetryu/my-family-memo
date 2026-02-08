import streamlit as st
import pandas as pd
import datetime
import requests

# 1. 기본 설정
st.set_page_config(page_title="우리 가족 메모장", page_icon="🏠")
st.title("👨‍👩‍👧‍👦 우리 가족 공동 메모장")

# 2. 주소 및 ID 설정 (주소 오타 방지를 위해 직접 입력)
SHEET_ID = "1MbL6-1fMZTBDdn_9CfyJkjrJsoqrYMEPquMWO7Cos8o"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
FORM_URL = "https://docs.google.com/forms/d/1lUs7h2cj-LGv-0RZjPWrsCLMJmt2CTzh9kvyzV8nlV0/formResponse"

ENTRIES = {
    "date": "entry.1691386708",
    "user": "entry.1460592934",
    "cat": "entry.348705031",
    "text": "entry.1509172605"
}

# 3. 데이터 로드 (에러 발생 시 상세 이유 출력)
@st.cache_data(ttl=5) # 5초마다 갱신
def load_data():
    try:
        df = pd.read_csv(READ_URL)
        return df
    except Exception as e:
        # 데이터 로드 실패 시 화면에 경고 표시 (데이터가 없어도 입력은 가능하게 함)
        st.warning(f"데이터를 불러오는 중입니다... (아직 저장된 내용이 없거나 시트가 비어있을 수 있습니다)")
        return pd.DataFrame(columns=["날짜", "작성자", "카테고리", "내용"])

# 4. 입력 UI (무조건 화면에 보이도록 설정)
with st.form("memo_form"):
    user = st.selectbox("누구신가요?", ["아빠", "엄마", "지빈", "도빈"])
    category = st.selectbox("카테고리", ["📅 일정", "🛒 장보기", "💡 아이디어", "💬 기타"])
    content = st.text_input("내용을 입력하세요")
    submit = st.form_submit_button("저장하기")

    if submit:
        if content:
            payload = {
                ENTRIES["date"]: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                ENTRIES["user"]: user,
                ENTRIES["cat"]: category,
                ENTRIES["text"]: content
            }
            try:
                response = requests.post(FORM_URL, data=payload)
                if response.status_code == 200:
                    st.success("✅ 저장 성공! (잠시 후 목록에 나타납니다)")
                else:
                    st.error(f"❌ 전송 실패 (에러 코드: {response.status_code})")
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
        # 최신 10개만 출력
        for i, row in df.iloc[::-1].head(10).iterrows():
            st.info(f"**[{row['카테고리']}] {row['내용']}** \n({row['작성자']} | {row['날짜']})")
    except Exception as e:
        st.error(f"목록 표시 중 오류: {e}")
else:
    st.write("표시할 메모가 없습니다.")
