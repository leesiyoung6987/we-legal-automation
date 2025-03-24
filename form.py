from fpdf import FPDF
import tempfile
from PIL import Image

def load_font():
    try:
        FPDF.add_font("NanumGothic", "", "NanumGothic.ttf", uni=True)
    except:
        pass

def generate_pdf(client_name, client_birth, client_address, client_phone,
                 agent_name, agent_birth, agent_address, agent_phone, agent_fax,
                 agency_name, agency_task, date):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("NanumGothic", "", "NanumGothic.ttf", uni=True)
    
    # 제목
    pdf.set_font("NanumGothic", size=18)
    pdf.cell(0, 10, "위 임 장", ln=True, align="C")
    pdf.ln(4)

    # 위임인 정보 (좌측정렬 적용)
    pdf.set_font("NanumGothic", size=12)
    pdf.cell(0, 8, "위임인    ______________________________________________", ln=True, align='L')
    pdf.cell(0, 8, f"성   명 : {client_name}", ln=True, align='L')
    pdf.cell(0, 8, f"생년월일 : {client_birth}", ln=True, align='L')
    pdf.cell(0, 8, f"주   소 : {client_address}", ln=True, align='L')
    pdf.cell(0, 8, f"전   화 : {client_phone}", ln=True, align='L')
    pdf.ln(4)

    # 수임인 정보 (좌측정렬 적용 및 '(리셋플러스)' 제거)
    pdf.cell(0, 8, "수임인    ______________________________________________", ln=True, align='L')
    pdf.cell(0, 8, f"성   명 : {agent_name}", ln=True, align='L')
    pdf.cell(0, 8, f"생년월일 : {agent_birth}", ln=True, align='L')
    pdf.cell(0, 8, f"주   소 : {agent_address}", ln=True, align='L')
    pdf.cell(0, 8, f"전   화 : {agent_phone}", ln=True, align='L')
    pdf.cell(0, 8, f"F A X : {agent_fax}", ln=True, align='L')
    pdf.ln(4)

    # 위임 설명
    pdf.set_font("NanumGothic", size=11)
    pdf.multi_cell(0, 7, "상기 위임인은 수임인에게 아래의 위임사항을 위임하며, 위임사실을 알리기 위해, 인감증명서를 첨부함과 동시에 동일한 인감도장을 날인합니다.", align='J')
    pdf.ln(2)

    # 위임사항 박스
    pdf.set_font("NanumGothic", size=14)
    pdf.cell(0, 10, "위 임 사 항", ln=True, align="C")
    pdf.ln(2)

    pdf.set_font("NanumGothic", size=11)
    x_start = 20
    y_start = pdf.get_y()
    pdf.rect(x_start, y_start, 170, 45)
    pdf.set_xy(x_start + 5, y_start + 3)
    content = (
        f"위임장 용도 : (개인회생 법원 제출용)\n\n"
        f"{agency_task}\n\n"
        "* 단면인쇄, 특수채권 포함 / 거래내역은 과거순(역순)\n"
        "첨부 : 인감증명서 1부, 신분증 사본"
    )
    pdf.multi_cell(160, 7, content, align="L")
    pdf.ln(42)

    # 날짜 및 서명 (4칸 위로 올림)
    pdf.set_xy(130, pdf.get_y() - 20)
    pdf.cell(0, 8, f"위임일자 : {date.strftime('%Y년 %m월 %d일')}", ln=True)
    pdf.set_x(130)
    pdf.cell(0, 8, f"위 임 인 : {client_name} (인)", ln=True)
    pdf.ln(8)

    # 귀중 (4칸 위로 올림 및 기관명 글씨 확대)
    pdf.set_font("NanumGothic", size=18)
    pdf.set_y(pdf.get_y() - 10)
    pdf.cell(0, 10, f"{agency_name} 귀중", ln=True, align="C")

    output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(output.name)
    return output.name

def convert_to_pdf(uploaded_file):
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as out:
            out.write(uploaded_file.read())
            return out.name
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(uploaded_file)
        pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        image.save(pdf_path, "PDF", resolution=100.0)
        return pdf_path
    else:
        raise ValueError("지원되지 않는 파일 형식입니다.")

