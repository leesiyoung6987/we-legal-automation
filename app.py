import streamlit as st
from datetime import datetime
import os
from form import load_font, generate_pdf, convert_to_pdf
from PyPDF2 import PdfMerger

# Load font
load_font()

# 수임인 정보
AGENTS = {
    "신현웅": {
        "name": "신현웅",
        "birth_full": "940317-1482816",
        "birth_short": "940317",
        "phone": "010-5679-3455",
        "address": "전주시 덕진구 기린대로 418 9층",
        "fax": "0502-989-9136",
        "id_file": "agents/신현웅.pdf"
    },
    "이성철": {
        "name": "이성철",
        "birth_full": "890215-1481926",
        "birth_short": "890215",
        "phone": "010-6554-2070",
        "address": "전주시 덕진구 기린대로 418 9층",
        "fax": "0502-989-9136",
        "id_file": "agents/이성철.pdf"
    },
    "이진우": {
        "name": "이진우",
        "birth_full": "900621-1481915",
        "birth_short": "900621",
        "phone": "010-7616-7233",
        "address": "전주시 덕진구 기린대로 418 9층",
        "fax": "0502-989-9136",
        "id_file": "agents/이진우.pdf"
    },
    "이시영": {
        "name": "이시영",
        "birth_full": "891102-1504316",
        "birth_short": "891102",
        "phone": "010-4228-6987",
        "address": "전주시 덕진구 기린대로 418 9층",
        "fax": "0502-989-9136",
        "id_file": "agents/이시영.pdf"
    }
}

st.set_page_config(page_title="위임장 자동 생성기")
st.title("📝 위임장 자동 생성기")

# 위임인 정보 입력
st.header("👤 위임인 정보")
client_name = st.text_input("성명")
client_birth = st.text_input("생년월일 (예: 900101)")
client_address = st.text_input("주소")
client_phone = st.text_input("전화번호")
client_id_file = st.file_uploader("위임인 신분증 업로드", type=["pdf", "jpg", "jpeg", "png"])

# 수임인 정보
st.header("📌 수임인 정보")
agent_selected = st.selectbox("수임인 이름을 선택하세요", list(AGENTS.keys()))
agent = AGENTS[agent_selected]

st.text_input("수임인 성명", value=agent["name"], disabled=True)
st.text_input("생년월일", value=agent["birth_short"], disabled=True)
st.text_input("주소", value=agent["address"], disabled=True)
st.text_input("전화번호", value=agent["phone"], disabled=True)
st.text_input("FAX", value=agent["fax"], disabled=True)

# 위임일자 입력
st.header("📅 위임일자 선택")
date = st.date_input("위임일자", datetime.today())

# 기관 정보 입력 (최대 20개)
st.header("🏦 기관별 위임내역 입력 (최대 20개)")
num_agencies = st.number_input("입력할 기관 개수 선택 (최대 20개)", min_value=1, max_value=20, value=1, step=1)

agency_data = []
tabs = st.tabs([f"기관 {i+1}" for i in range(num_agencies)])

for idx, tab in enumerate(tabs):
    with tab:
        agency_name = st.text_input(f"{idx+1}번째 기관명 입력", key=f"agency_name_{idx}")
        agency_task = st.text_area(f"{idx+1}번째 위임내역 입력", key=f"agency_task_{idx}")
        agency_data.append({"name": agency_name, "task": agency_task})

# PDF 생성 및 병합 버튼
if st.button("📄 전체 PDF 생성 및 다운로드"):
    if not all([client_name, client_birth, client_address, client_phone, client_id_file]):
        st.warning("모든 위임인 정보를 입력하고 위임인 신분증을 업로드해주세요.")
    elif not all([agency["name"] and agency["task"] for agency in agency_data]):
        st.warning("모든 기관명과 위임내역을 빠짐없이 입력해주세요.")
    else:
        with st.spinner("전체 PDF를 생성 중입니다..."):
            client_id_path = convert_to_pdf(client_id_file)
            merger = PdfMerger()
            temp_files = [client_id_path]  # 삭제할 임시 파일 관리

            try:
                for agency in agency_data:
                    pdf_path = generate_pdf(
                        client_name, client_birth, client_address, client_phone,
                        agent["name"], agent["birth_short"], agent["address"],
                        agent["phone"], agent["fax"],
                        agency["name"], agency["task"], date
                    )

                    merger.append(pdf_path)
                    merger.append(client_id_path)
                    merger.append(agent["id_file"])

                    temp_files.append(pdf_path)

                merged_pdf_path = "merged_all_documents.pdf"
                with open(merged_pdf_path, "wb") as f_out:
                    merger.write(f_out)

                merger.close()  # 병합 종료 후 닫기

                # 최종 PDF 다운로드 버튼
                with open(merged_pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 전체 통합 PDF 다운로드",
                        data=f,
                        file_name="전체_위임장_통합.pdf",
                        mime="application/pdf"
                    )

            finally:
                # 파일 닫은 후 삭제하기
                for path in temp_files + [merged_pdf_path]:
                    if os.path.exists(path):
                        os.remove(path)
