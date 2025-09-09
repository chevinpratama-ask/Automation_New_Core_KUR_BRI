import os
import json
import textwrap
from fpdf import FPDF
import datetime
import random

project_code = "KP.ACS.09787.9888"
project_name = "H2H New Core KUR BRI"
project_type = "New"
core_noncore = "core"
tester_name = "Chevin & Annisa"
module_name = "New Core KUR BRI"
testcase_id = "TC01"
testcase_name ="Cek IJP Flag"
jenis_test = "Positive"
actual_result = "Berhasil validasi IJP KUR antara H2H dan DB"
expected_result= "Sistem akan memvalidasi IJP KUR H2H dan DB"
platform = "Windows 11 64 Bit"
browser = "Chrome"

# =================== Fungsi PDF Helper =================== #
def write_payload_response(pdf: FPDF, payload: dict, response: dict, step_index: int = 1):
    pdf.set_font("Arial", size=8)

    payload_lines = json.dumps(payload, indent=4, ensure_ascii=False).split("\n")
    response_lines = json.dumps(response, indent=4, ensure_ascii=False).split("\n")
    max_lines = max(len(payload_lines), len(response_lines))

    box_width = 85
    left_x = 20
    line_height = 4.5
    margin_bottom = 15

    # ==== Header Box ====
    def draw_header(y):
        pdf.set_fill_color(230, 230, 230)
        pdf.set_xy(left_x, y)
        pdf.cell(box_width, 8, "Payload", border=1, fill=True, align="C")
        pdf.set_xy(left_x + box_width, y)
        pdf.cell(box_width, 8, "Response", border=1, fill=True, align="C")
        return y + 8

    # Cetak judul step (hanya sekali di awal
    top_y = draw_header(pdf.get_y())
    start_y = top_y

    for i in range(max_lines):
        payload_line = payload_lines[i] if i < len(payload_lines) else ""
        response_line = response_lines[i] if i < len(response_lines) else ""

        # Ukur tinggi payload
        pdf.set_xy(left_x + 1, top_y)
        payload_split = pdf.multi_cell(box_width - 2, line_height, payload_line, border=0, split_only=True)
        h_payload = len(payload_split) * line_height if payload_split else line_height

        # Ukur tinggi response
        pdf.set_xy(left_x + box_width + 1, top_y)
        response_split = pdf.multi_cell(box_width - 2, line_height, response_line, border=0, split_only=True)
        h_response = len(response_split) * line_height if response_split else line_height

        max_h = max(h_payload, h_response)

        # Kalau tidak muat, tutup border lalu pindah halaman
        if top_y + max_h > pdf.h - margin_bottom:
            # Tutup border halaman sebelumnya
            full_height = top_y - start_y
            pdf.set_draw_color(0, 0, 0)
            pdf.rect(left_x, start_y, box_width * 2, full_height)
            pdf.line(left_x + box_width, start_y, left_x + box_width, start_y + full_height)

            # Pindah halaman
            pdf.add_page()
            pdf.set_font("Arial", size=8)
            top_y = draw_header(pdf.get_y())
            start_y = top_y

        # Cetak payload
        pdf.set_xy(left_x + 1, top_y)
        pdf.multi_cell(box_width - 2, line_height, payload_line, border=0)

        # Cetak response
        pdf.set_xy(left_x + box_width + 1, top_y)
        pdf.multi_cell(box_width - 2, line_height, response_line, border=0)

        # Naikkan Y
        top_y += max_h

    # Tutup border akhir (halaman terakhir)
    full_height = top_y - start_y
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(left_x, start_y, box_width * 2, full_height)
    pdf.line(left_x + box_width, start_y, left_x + box_width, start_y + full_height)


def write_verifikasi_database_auto(
    pdf: FPDF, 
    query: str, 
    db_data: dict, 
    step_index: int,
    min_col_width=25, 
    max_horizontal_cols=6, 
    label_shift=5
):
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_x(pdf.l_margin)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    cell_height = 5  # tinggi baris untuk query

    # ========== TAMPILKAN QUERY ==========
    pdf.set_font("Courier", 'I', 9)
    pdf.cell(0, cell_height, "Query:", ln=True)

    query_str = str(query).strip() if query else ""

    if query_str:
        query_lines = query_str.splitlines()
        for line in query_lines:
            if pdf.get_y() + cell_height > pdf.h - 15:  # cek batas bawah halaman
                pdf.add_page()
            pdf.set_x(pdf.l_margin)  # mulai dari margin kiri
            pdf.multi_cell(usable_width, cell_height, line, border=0)
    else:
        pdf.multi_cell(usable_width, cell_height, "(kosong)", border=0)

    pdf.ln(4)

    # ========== TAMPILKAN DATA ==========
    if not db_data:
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(0, 8, "Tidak ada hasil dari query.", ln=True)
        return

    fields = list(db_data.keys())
    values = list(db_data.values())
    num_cols = len(fields)

    # ========= VERTICAL LAYOUT =========
    if num_cols > max_horizontal_cols or (usable_width / num_cols) < min_col_width:
        pdf.set_font("Arial", size=9)
        cell_height = 6
        label_width = min(60, usable_width * 0.35) + label_shift
        value_width = usable_width - label_width

        for field, value in zip(fields, values):
            pdf.set_x(pdf.l_margin)

            val_str = str(value) if value is not None else "-"
            max_chars = max(15, int(value_width / pdf.get_string_width('M')))
            wrapped_lines = textwrap.wrap(val_str, width=max_chars)
            wrapped_text = "\n".join(wrapped_lines)

            estimated_height = max(1, len(wrapped_lines)) * cell_height
            if pdf.get_y() + estimated_height > pdf.h - 15:
                pdf.add_page()

            # Label (pakai border & fill abu-abu)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(label_width, cell_height, str(field), border=1, fill=True)

            # Value (pakai border, multi-line)
            pdf.multi_cell(value_width, cell_height, wrapped_text, border=1)
    else:
        # ========= HORIZONTAL LAYOUT =========
        pdf.set_font("Arial", size=8)
        cell_height = 6
        column_width = usable_width / num_cols
        margin_bottom = 15

        def draw_header():
            pdf.set_x(pdf.l_margin + label_shift)
            pdf.set_fill_color(230, 230, 230)
            for key in fields:
                pdf.cell(column_width, cell_height, str(key), border=1, fill=True, align='C')
            pdf.ln(cell_height)

        draw_header()

        wrapped_values = []
        max_chars = max(5, int(column_width / pdf.get_string_width('M')))
        for val in values:
            lines = textwrap.wrap(str(val) if val is not None else "-", width=max_chars)
            wrapped_values.append(lines)

        max_lines = max(len(lines) for lines in wrapped_values)

        for i in range(max_lines):
            if pdf.get_y() + cell_height > pdf.h - margin_bottom:
                pdf.add_page()
                draw_header()

            pdf.set_x(pdf.l_margin + label_shift)
            y_start = pdf.get_y()
            max_height = 0
            col_texts = []

            for col_lines in wrapped_values:
                text = col_lines[i] if i < len(col_lines) else ""
                height = max(cell_height, len(textwrap.wrap(text, width=max_chars)) * cell_height)
                max_height = max(max_height, height)
                col_texts.append(text)

            x_start = pdf.get_x()
            for text in col_texts:
                pdf.multi_cell(column_width, cell_height, text, border=1, align='L', ln=3)
                x_start += column_width
                pdf.set_xy(x_start, y_start)

            pdf.ln(max_height)


def write_verifikasi_database_multi(pdf: FPDF, query: str, db_rows: list[dict], step_index: int):
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.set_x(pdf.l_margin)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    cell_height = 5

    # ========== TAMPILKAN QUERY ==========
    pdf.set_font("Courier", 'I', 9)
    pdf.cell(0, cell_height, "Query:", ln=True)

    query_str = str(query).strip() if query else ""

    if query_str:
        query_lines = query_str.splitlines()
        for line in query_lines:
            if pdf.get_y() + cell_height > pdf.h - 15:  # cek batas bawah halaman
                pdf.add_page()
            pdf.set_x(pdf.l_margin)  # mulai dari margin kiri
            pdf.multi_cell(usable_width, cell_height, line, border=0)
    else:
        pdf.multi_cell(usable_width, cell_height, "(kosong)", border=0)

    pdf.ln(4)

    # ========== TAMPILKAN DATA (TABLE) ==========
    if not db_rows:
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(0, 8, "Tidak ada hasil dari query.", ln=True)
        return

    fields = list(db_rows[0].keys())
    num_cols = len(fields)
    col_width = usable_width / num_cols

    # Header
    pdf.set_font("Arial", 'B', 8)
    pdf.set_fill_color(230, 230, 230)
    for f in fields:
        pdf.cell(col_width, cell_height, str(f), border=1, fill=True, align="C")
    pdf.ln(cell_height)

    # Rows
    pdf.set_font("Arial", '', 8)
    for row in db_rows:
        if pdf.get_y() + cell_height > pdf.h - 15:
            pdf.add_page()
            # redraw header
            pdf.set_font("Arial", 'B', 8)
            pdf.set_fill_color(230, 230, 230)
            for f in fields:
                pdf.cell(col_width, cell_height, str(f), border=1, fill=True, align="C")
            pdf.ln(cell_height)
            pdf.set_font("Arial", '', 8)

        for f in fields:
            val = str(row.get(f, "")) if row.get(f, "") is not None else "-"
            pdf.cell(col_width, cell_height, val, border=1)
        pdf.ln(cell_height)


def verify_db_vs_payload(db_row: dict, payload: dict) -> dict:
    """
    Compare DB vs Payload and return dict {field: (status, db_val, payload_val)}
    Status hanya 'MATCH' atau 'MISMATCH'
    """
    results = {}
    for key, db_value in db_row.items():
        payload_value = payload.get(key)

        db_str = "" if db_value is None else str(db_value).strip()
        payload_str = "" if payload_value is None else str(payload_value).strip()

        if db_str == payload_str:
            results[key] = ("MATCH", db_str, payload_str)
        else:
            results[key] = ("MISMATCH", db_str, payload_str)
    return results


def write_verifikasi_result(pdf: FPDF, results: dict):
    margin = 20
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)

    headers = ["Field", "DB Value", "Payload Value", "Status"]
    col_widths = [55, 50, 50, 15]
    line_height = 5

    # Hapus add_page() awal
    # pdf.add_page()

    # Judul ditulis **setelah test step**
    pdf.ln(3)  # beri jarak dari step sebelumnya
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(sum(col_widths), 8, "Hasil Verifikasi DB vs Payload", border=0, ln=True, align="C")
    pdf.ln(2)

    # Fungsi menulis header tabel
    def add_table_header():
        pdf.set_font("Arial", 'B', 8)
        pdf.set_fill_color(200, 200, 200)
        pdf.set_x(margin)
        for i, header in enumerate(headers):
            pdf.multi_cell(col_widths[i], line_height, header, border=1, fill=True, align='C')
            pdf.set_xy(margin + sum(col_widths[:i+1]), pdf.get_y() - line_height)
        pdf.ln(line_height)
        pdf.set_font("Arial", '', 8)

    add_table_header()

    # Fungsi wrap teks berdasarkan lebar kolom
    def split_text(text, col_width):
        pdf.set_font("Arial", '', 8)
        words = str(text).split()
        lines = []
        current_line = ""
        for word in words:
            if pdf.get_string_width((current_line + " " + word).strip()) < col_width - 1:
                current_line = (current_line + " " + word).strip()
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines if lines else ['']

    for key, (status, db_val, payload_val) in results.items():
        # cek margin bawah
        if pdf.get_y() > pdf.h - 30:
            pdf.add_page()
            add_table_header()

        cols_lines = [
            split_text(key, col_widths[0]),
            split_text(db_val, col_widths[1]),
            split_text(payload_val, col_widths[2]),
            ["OK" if status == "MATCH" else "X"]
        ]

        max_lines = max(len(lines) for lines in cols_lines)
        row_height = max_lines * line_height
        x_start = margin
        y_start = pdf.get_y()

        # warna fill jika mismatch
        if status == "MATCH":
            fill = False
        else:
            pdf.set_fill_color(255, 255, 0)
            fill = True

        aligns = ['L', 'L', 'L', 'C']
        for i, lines in enumerate(cols_lines):
            pdf.set_xy(x_start + sum(col_widths[:i]), y_start)
            for line in lines:
                pdf.multi_cell(col_widths[i], line_height, line, border=1, fill=fill, align=aligns[i])
                pdf.set_x(x_start + sum(col_widths[:i]))
            extra_lines = max_lines - len(lines)
            for _ in range(extra_lines):
                pdf.multi_cell(col_widths[i], line_height, "", border=1, fill=fill)
                pdf.set_x(x_start + sum(col_widths[:i]))

        pdf.set_y(y_start + row_height)
        pdf.set_text_color(0, 0, 0)


#================No Rekening Acak 15=======#
def generate_no_rekening_acak():
    """Menghasilkan nomor rekening acak sepanjang 14 digit (string)."""
    return ''.join([str(random.randint(0, 9)) for _ in range(15)])

# =================== Class PDF =================== #
class CustomPDF(FPDF):
    def header(self):
        if self.page_no() > 2:
            self.set_font("Arial", 'B', 10)
            self.set_fill_color(255, 255, 255)

            # Ukuran tabel
            page_margin = 20
            total_width = 210 - 2 * page_margin
            logo_width = 50
            right_width = 30
            center_width = total_width - logo_width - right_width
            cell_height = 7
            top_y = self.get_y()

            logo_x = page_margin
            logo_y = top_y
            logo_cell_width = logo_width
            logo_cell_height = cell_height * 3  # tinggi kolom logo (3 baris)

            # ===== CELL KIRI (Logo) =====
            self.set_xy(logo_x, logo_y)
            self.cell(logo_cell_width, logo_cell_height, "", border=1)

            # ====== TAMBAHKAN LOGO ======
            logo_path = "logo askrindo.png"
            if os.path.exists(logo_path):
                # Ukuran asli gambar (ambil langsung)
                from PIL import Image
                img = Image.open(logo_path)
                img_w, img_h = img.size
                aspect_ratio = img_h / img_w

                # Hitung ukuran gambar supaya muat & rata tengah
                max_img_width = logo_cell_width - 6
                max_img_height = logo_cell_height - 4
                draw_w = max_img_width
                draw_h = draw_w * aspect_ratio

                if draw_h > max_img_height:
                    draw_h = max_img_height
                    draw_w = draw_h / aspect_ratio

                img_x = logo_x + (logo_cell_width - draw_w) / 2
                img_y = logo_y + (logo_cell_height - draw_h) / 2
                self.image(logo_path, x=img_x, y=img_y, w=draw_w, h=draw_h)

            # ===== TABEL TENGAH (3 baris) =====
            self.set_font("Arial", '', 10)

            self.set_x(logo_x + logo_cell_width)
            self.cell(center_width, cell_height, "ASKRINDO", border=1, ln=2, align='C')

            self.set_x(logo_x + logo_cell_width)
            self.cell(center_width, cell_height, "DOKUMEN HASIL TESTING", border=1, ln=2, align='C')

            self.set_x(logo_x + logo_cell_width)
            self.cell(center_width, cell_height, "H2H Core KUR BRI", border=1, ln=0, align='C')

            # ===== CELL KANAN (UAT) =====
            self.set_xy(logo_x + logo_cell_width + center_width, logo_y)
            self.set_font("Arial", '', 10)
            self.cell(right_width, logo_cell_height, "SIT", border=1, align='C')

            # Spasi ke bawah
            self.ln(logo_cell_height + 8)

        # Jangan tampilkan nomor halaman di halaman pertama

    def footer(self):
        if self.page_no() == 0:
            return
        self.set_y(-15)
        self.set_font("Arial", size=8)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)

        box_width = 8
        box_height = 8
        page_number_text = f"{self.page_no() -0}"  # agar halaman kedua jadi "1"

        x_position = self.w - self.r_margin - box_width
        y_position = self.get_y()

        self.rect(x_position, y_position, box_width, box_height)       # Membuat kotak outline
        self.set_xy(x_position, y_position)
        self.cell(box_width, box_height, txt="", align='C', fill=True)


def generate_pdf_report (
    test_steps_rendered,
    screenshot_rendered,
    Project="Aplikasi SimpleRisk",
    testcase_id= testcase_id,
    testcase_name= testcase_name,
    expected_result = expected_result,
    actual_result=None,
    logo_path="logo askrindo.png",
    tester="chevin",
    status=None,
    screenshot_paths=None,
    failed_step_index = None,
    tanggal_revisi_1 = "22/07/2025",
    tanggal_revisi_2 = "23/07/2025",
    tanggal_revisi_3 = "24/07/2025",
    versi_1 = "V.I.I",
    versi_2 = "V.I.II",
    versi_3 = "V.I.III",
    keterangan_revisi_1 = "Initial Doc",
    keterangan_revisi_2 = "Dokument Hasil Testing SIT Chevin Rifan Pratama Halloha genter",
    keterangan_revisi_3 = "Final Doc",
    pic_1 = "Chevin & Annisa",
    pic_2 = "Chevin & Annisa",
    pic_3 = "Chevin & Annisa",
    payload=None,
    response=None,
    payload_step_index=None,
    db_query=None,             
    db_data=None,               
    db_step_index=None,
    nomor_rekening_pinjaman=None,
    db_verification_result=None,
    db_verification_step_index=None,
    db_query_step4=None,
    db_result_step4=None,
    db_step_index_step4=None    
):
    #-------Simpan Folder PDF-----------#
    waktu = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_base = f"{testcase_id}_{testcase_name.replace(' ', '_')}"

    if status == "Passed":
        folder = os.path.join(folder_base, "Laporan_Passed")
        nama_file = f"Laporan_Passed_{testcase_name.replace(' ', '_')}_{waktu}.pdf"
    else:
        folder = os.path.join(folder_base, "Laporan_Failed")
        nama_file = f"Laporan_Failed_{testcase_name.replace(' ', '_')}_{waktu}.pdf"

    os.makedirs(folder, exist_ok=True)  # pastikan folder dibuat
    path_to_pdf = os.path.join(folder, nama_file)


    # Buat nama file PDF
    pdf_path = os.path.join(folder, nama_file)
    print(f"PDF akan disimpan di: {pdf_path}")
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)


# #== Halaman 1: Judul =====
    pdf.add_page()

    if os.path.exists(logo_path):
        pdf.image(logo_path, x=20, y=16, w=45)  # Rata kiri 20mm
    else:
        print("Logo tidak ditemukan")

    pdf.set_font("Arial", 'B', 25)
    pdf.set_xy(20, 60)
    pdf.cell(170, 12, "Laporan Hasil Pengujian SIT", ln=True, align='L')  # Lebar 170mm
    pdf.set_x(20)
    pdf.cell(170, 12, "New Core KUR BRI", ln=True, align='L')
    pdf.set_x(20)
    pdf.cell(170, 12, "04/09/2025", ln=True, align='L')
    pdf.set_x(20)
    pdf.cell(170, 12, "V.I.II", ln=True, align='L')

    # ===== Halaman 2: Judul =====
    pdf.add_page()

    if os.path.exists(logo_path):
        pdf.image(logo_path, x=20, y=16, w=45)
    else:
        print("Logo tidak ditemukan")

    pdf.set_font("Arial", 'B', 15)
    pdf.set_xy(20, 45)
    pdf.cell(170, 12, "Daftar Revisi", ln=True, align='L')
  
    summary_data = [
    ["Tanggal", "Versi", "Keterangan Revisi", "PIC"],
    [tanggal_revisi_1, versi_1, keterangan_revisi_1, pic_1],
    [tanggal_revisi_2, versi_2, keterangan_revisi_2, pic_2],
    [tanggal_revisi_3, versi_3, keterangan_revisi_3, pic_3],
]

    col_widths = [40, 25, 80, 30]  # Widths: Tanggal, Versi, Keterangan, PIC
    start_x = 20
    line_height = 8

    for i, row in enumerate(summary_data):
        pdf.set_x(start_x)
    
        if i == 0:
            #header
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font("Arial", 'B', 10)
            for j, cell in enumerate(row):
               pdf.cell(col_widths[j], line_height, str(cell), border=1, fill=True, align='c')
            pdf.ln(line_height)  # hanya sekali pindah baris setelah header
        else:
            pdf.set_font("Arial", '', 9)
            y_start = pdf.get_y()
            x = start_x

        # MultiCell hanya untuk kolom ke-3 (Keterangan Revisi)
            pdf.set_xy(x + col_widths[0] + col_widths[1], y_start)
            multicell_y_before = pdf.get_y()
            pdf.multi_cell(col_widths[2], line_height-3, str(row[2]), border=1)
            multicell_y_after = pdf.get_y()
            height = multicell_y_after - multicell_y_before

        # Cetak kolom Tanggal & Versi
            pdf.set_xy(x, y_start)
            pdf.cell(col_widths[0], height, str(row[0]), border=1)
            pdf.cell(col_widths[1], height, str(row[1]), border=1)

        # Cetak kolom PIC
            pdf.set_xy(x + col_widths[0] + col_widths[1] + col_widths[2], y_start)
            pdf.cell(col_widths[3], height, str(row[3]), border=1)

        # Pindah ke baris berikutnya
            pdf.set_y(y_start + height)


    # ===== Halaman 3: Header, Logo, Ringkasan =====
    pdf.add_page()
    pdf.set_y(40)
    pdf.set_font("Arial", size=10)

    summary_data1 = [
    ["TestCaseID", testcase_id],
    ["TestCaseName", testcase_name],
    ["Jenis Test", jenis_test],
    ["Date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ["Tester", tester],
    ["Status", status],
    ["Expected Result", expected_result],
]

        # Ukuran dan posisi
    cell_height = 6
    left_col_width = 40
    right_col_width = 130
    x_start = 20

    for key, value in summary_data1:
        y_start = pdf.get_y()

        if key in ["TestCaseName", "Expected Result"]:
            # Hitung tinggi value saja
            def get_text_height(text, width):
                temp = FPDF()
                temp.add_page()
                temp.set_font("Arial", size=10)
                temp.set_xy(0, 0)
                temp.multi_cell(width, cell_height, str(text))
                return temp.get_y()

            value_height = get_text_height(value, right_col_width)
            row_height = max(value_height, cell_height)

            # Draw background & border untuk key
            pdf.set_fill_color(230, 230, 230)
            pdf.rect(x_start, y_start, left_col_width, row_height, 'F')
            pdf.rect(x_start, y_start, left_col_width, row_height)

            # Draw border untuk value
            pdf.rect(x_start + left_col_width, y_start, right_col_width, row_height)

            # Isi key
            pdf.set_xy(x_start, y_start)
            pdf.multi_cell(left_col_width, cell_height, str(key), border=0)

            # Isi value
            pdf.set_xy(x_start + left_col_width, y_start)
            pdf.multi_cell(right_col_width, cell_height, str(value), border=0)

            pdf.set_y(y_start + row_height)

        else:
            pdf.set_x(x_start)
            pdf.set_fill_color(230, 230, 230)
            pdf.cell(left_col_width, cell_height, str(key), border=1, fill=True)
            pdf.cell(right_col_width, cell_height, str(value), border=1)
            pdf.ln()

     # Data
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    pdf.set_x(20)
    # Judul Seksi Data
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, "Data:", ln=True)
    pdf.set_font("Arial", size=11)


    # label_width = 60
    # colon_width = 4
    # value_width = 136

    # def print_data_row(label, value):
    #     pdf.set_x(20)
    #     pdf.cell(label_width, 6, label, ln=0)
    #     pdf.cell(colon_width, 6, ":", ln=0)
    #     pdf.cell(value_width, 6, value, ln=1)

    # print_data_row("No Request", nomor_reqeuest)
    # print_data_row("No Polis", nomor_polis)
    # print_data_row("No Rekening", nomor_rekening)

    # pdf.ln(3)

#===================================
    y_start = 35
    max_y = pdf.h - 15
    pdf.set_auto_page_break(auto=False)
    pdf.set_font("Arial", size=11)

    for i, step in enumerate(test_steps_rendered):
        pdf.set_font("Arial", size=11)
        current_y = pdf.get_y()

        # === Estimasi tinggi konten ===
        estimated_height = 0

        # 1. Judul step
        estimated_height += 8 + (pdf.get_string_width(step) / 170 * 8)

        # 2. Gambar
        image_height = 0
        image_paths = []
        if i < len(screenshot_paths):
            img_list = screenshot_paths[i] if isinstance(screenshot_paths[i], list) else [screenshot_paths[i]]
            for img in img_list:
                if img and os.path.exists(img):
                    image_paths.append(img)
                    image_height += 100 + 3  # tinggi + margin bawah
        estimated_height += image_height

        # 3. Payload & response
        if payload and response and payload_step_index == i:
            estimated_height += 60  # asumsi default, atau buat fungsi estimasi lebih akurat

        # 4. Query
        if db_query and db_data and db_step_index == i:
            query_lines = db_query.count('\n') + 1
            estimated_height += query_lines * 5 + 10  # estimasi multiline query

        # === Kalau tidak muat, add_page dulu ===
        if current_y + estimated_height > max_y:
            pdf.add_page()
            pdf.set_y(y_start)
            current_y = pdf.get_y()

        # === Cetak Judul Step ===
        if failed_step_index is not None and i == failed_step_index:
            pdf.set_text_color(255, 0, 0)
        else:
            pdf.set_text_color(0, 0, 0)

        pdf.set_x(20)
        pdf.multi_cell(170, 8, step, border=0)
        after_text_y = pdf.get_y()

    # === Gambar ===
        for img_path in image_paths:
            if pdf.get_y() + 100 > max_y:
                pdf.add_page()
                pdf.set_y(y_start)

            pdf.set_x(20)
            pdf.image(img_path, x=20, w=170)
            pdf.ln(3)

        # === Payload / Response ===
        if payload and response and payload_step_index == i:
            write_payload_response(pdf, payload, response, step_index=i + 1)
            pdf.ln(5)

        # === DB Query & Data (Step 2) ===
        if db_query and db_data and db_step_index == i:
            write_verifikasi_database_auto(pdf, db_query, db_data, step_index=i + 1)
            pdf.ln(5)

        # === Verifikasi DB vs Payload (Step 3) ===
        if db_verification_result and db_verification_step_index == i:
            write_verifikasi_result(pdf, db_verification_result)
            pdf.ln(5)

        # === DB Query & Data (Step 4) ===
        if db_query_step4 and db_result_step4 and db_step_index_step4 == i:
            write_verifikasi_database_multi(pdf, db_query_step4, db_result_step4, step_index=i + 1)
            pdf.ln(5)



    if status != "Passed":
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        pdf.ln(3)

        pdf.set_x(20)
        pdf.cell(170, 10, "Log Error / Gagal:", ln=True)

        pdf.set_font("Arial", '', 11)
        pdf.set_x(20)
        pdf.multi_cell(170, 6, actual_result) 
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        pdf.ln(3)
        pdf.set_x(20)
        combined_text = f"Actual Result : {actual_result}"
        pdf.multi_cell(170, 6, combined_text)
    
# Simpan PDF

    pdf.output(pdf_path)
    print(f"PDF berhasil disimpan ke: {pdf_path}")
    return pdf_path
