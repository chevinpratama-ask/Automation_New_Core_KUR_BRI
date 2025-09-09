import os
import time
import datetime
import pytest
# from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageOps
import requests
# import logging
# import traceback
# import sys
# import math

# Import PDF Generator
from report.pdf_generator import *
from utils.db_utils import *

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

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()

# ========== Simpan Screenshot ========== #
def save_screenshot(
    driver,
    elements=None,
    base_name="screenshot",
    highlight=False,
    testcase_id=None,
    testcase_name=None,
):
    folder = os.path.join(f"{testcase_id}_{testcase_name.replace(' ', '_')}", "Screenshots")
    os.makedirs(folder, exist_ok=True)

    waktu = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{waktu}.png"
    path = os.path.join(folder, filename)

    original_styles = []

    # ====== Tambahkan highlight jika diminta ======
    if highlight and elements:
        for elem in elements:
            original_style = elem.get_attribute("style")
            original_styles.append(original_style)
            driver.execute_script("arguments[0].setAttribute('style', arguments[1])", elem, "border: 3px solid red;")
        time.sleep(0.2)

    # Screenshot disimpan (sementara)
    driver.save_screenshot(path)

    # Hapus highlight jika ada
    if highlight and elements:
        for elem, style in zip(elements, original_styles):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1])", elem, style)

    # Tambahkan border hitam ke screenshot
    img = Image.open(path)

    # Ganti nama sesuai apakah pakai highlight atau tidak
    suffix = "_highlight" if highlight else "_border"
    bordered_path = f"{os.path.splitext(path)[0]}{suffix}.png"

    bordered_img = ImageOps.expand(img, border=2, fill='black')
    bordered_img.save(bordered_path)

    # Hapus file asli tanpa border
    os.remove(path)

    print(f"Screenshot disimpan di: {bordered_path}")
    return bordered_path


# ========== Test Case 01 ========== #
@pytest.mark.h2h
def test_create_polis(driver):
    test_steps_rendered = []
    screenshot_rendered = []
    db_result = {}
    db_query = {}
    nomor_rekening_pinjaman = ""
    payload = {}
    response_json = {}
    db_verification_result = {}
    db_query_step4 = {}
    db_result_step4 = {}

    try:
        # ================= STEP 1: Hit API =================
        test_steps_rendered.append("[Test_Step_1]: Hit Postman Covering Validation")
        screenshot_rendered.append(None)
        API_ENDPOINT = "http://10.100.10.47:8084/BRISURF/CoveringValidation"
        headers = {"Content-Type": "application/json"}


        payload = {  
   
            "RequestId": "12432660a000",
            "FIDProgram": 179,
            "NamaProgram": "Askred KUR Mikro KMK Askrindo",
            "FIDKategoriAsuransi": 1,
            "FIDJenisAsuransi": 1,
            "NomorRekeningPinjaman": generate_no_rekening_acak(),
            "CIFRekeningPinjaman": "SFMKC55",
            "LoanType": "SK",
            "LoanTypeDesc": "Askred KUR Mikro KMK Askrindo",
            "JangkaWaktuBulan": 36,
            "JangkaWaktuPilihan": 0,
            "SukuBungaPinjamanTahun": 0.06,
            "Plafon": 20000000,
            "Outstanding": 10000000,
            "TotalEksposure": 0,
            "FlagCorona": 0,
            "FlagRestruk": 0,
            "Kolektabilitas": 1,
            "TanggalAkadKreditRestruk": "20/10/2024",
            "TanggalKreditRestruk": "20/10/2024",
            "TanggalAkadKredit": "20/10/2024",
            "TanggalRealisasi": "20/10/2024",
            "TanggalJatuhTempo": "20/10/2027",
            "TanggalPembentukanRekening": "20/10/2024",
            "UnitCode": "3049",
            "UnitDesc": "BRI, UNIT NANGA PINOH",
            "BranchCode": "3049",
            "BranchDesc": "KC Jakarta Pasar Minggu",
            "RegionCode": "I",
            "RegionDesc": "DKI2                                    ",
            "MakerBranch": "0953",
            "MakerID": "0953891",
            "NomorPerjanjianKredit": "74574/953/08/2021",
            "NilaiLikuiditas": 0,
            "SektorEkonomi": "050111",
            "FIDKategoriJenisFasilitas": 0,
            "NamaPeserta": "DEB19012023",
            "NomorIdentitas": "1204120107899999",
            "NPWP": "TESTA010101034",
            "Email": "test@gmail.com",
            "TanggalLahir": "01/07/1990",
            "TempatLahir": "Bandung",
            "FIDJenisKelamin": 9,
            "JenisKelamin": "BADAN USAHA",
            "FIDPendidikan": 6,
            "Pendidikan": "LAINNYA",
            "FIDPekerjaan": 99,
            "Pekerjaan": "LAIN-LAIN",
            "FIDStatusPernikahan": 9,
            "StatusPernikahan": "Menikah",
            "NomorHP": "0812890080900",
            "Alamat1": "Alamat A",
            "Alamat2": "Alamat B",
            "Alamat3": "Alamat C",
            "Alamat4": "RAGUNAN KEL,Jakarta Selatan, Wil. Kota",
            "KodePos": 12550,
            "KodeKabupatenKota": "0394",
            "NamaPerusahaanInti": "Perusahaan 1",
            "TanggalMulaiUsaha": "01/01/2000",
            "NomorIjinUsaha": "1234567",
            "ModalUsaha": 10000000,
            "AlamatUsaha": "Alamat 1",
            "JumlahTenagaKerja": 42,
            "NomorRekeningPinjamanSebelumnya": "",
            "NomorPesertaSebelumnya": "",
            "NominalPremiSebelumnya": 0,
            "FIDJenisAgunan": "0",
            "FIDAgunan": "0",
            "KodeJenisPenggunaan": "",
            "KodePosAgunan": "",
            "AlamatAgunan": "",
            "TahunAgunan": 0,
            "KodeOkupasi": "",
            "FlagPasar": 2,
            "KodePasar": "",
            "RangkaBangunan": "",
            "PenutupAtap": "",
            "BahanLantai": "",
            "BahanDinding": "",
            "JumlahLantai": 0,
            "PlatNomorKendaraan": "B-123-DE",
            "NomorBuktiKepemilikan": "",
            "NomorRangka": "",
            "NomorSeri": "",
            "NomorMesin": "",
            "Warna": "",
            "MerkKendaraan": "",
            "MerkTipeKendaraan": "",
            "KodeJenisKendaraan": "",
            "NominalObjekPertanggungan": 0,
            "DeskripsiAgunan": "",
            "TanggalMulaiChannel": "01/01/1900",
            "TanggalAkhirChannel": "01/01/1900",
            "FIDCashVault": 0,
            "FIDCashPickup": 0,
            "LokasiResiko": "",
            "KodePosResiko": "",
            "NamaAhliWaris": "",
            "TanggalLahirAhliWaris": "01/01/1900",
            "FIDJenisKelaminAhliWaris": 0,
            "JenisKelaminAhliWaris": "Perempuan",
            "AlamatAhliWaris": "",
            "NomorTelpAhliWaris": "",
            "FIDHubunganAhliWaris": 0,
            "HubunganAhliWaris": "",
            "NomorRekeningSimpanan": "",
            "CIFRekeningSimpanan": "",
            "PromoCode": "",
            "FIDScheduleCoveringNextPremium": 0,
            "NominalObjekPertanggunganValas": 0,
            "Currency": "",
            "NilaiKurs": 0,
            "TanggalKurs": "01/01/1900 00:00:00",
            "NomorRekeningDebet": "",
            "FIDChannelCovering": "1234",
            "ChannelCovering": "SSIS Push Covering Restruct Submission",
            "PNReferal": ""
        }
        nomor_rekening_pinjaman = payload["NomorRekeningPinjaman"]

        response = requests.post(API_ENDPOINT, headers=headers, json=payload, verify=False)
        try:
            response_json = response.json()
        except ValueError:
            pytest.fail(f"Response bukan JSON valid:\n{response.text}")

        if response_json.get("ResponseCode") != "00":
            code = response_json.get("ResponseCode")
            desc = response_json.get("ResponseDescription", "No description provided")
            pytest.fail(f"Code bukan '00' ({code}), ResponseDescription: {desc}, testing dihentikan:\n{json.dumps(response_json, indent=4, ensure_ascii=False)}")

        time.sleep(2)

        # if not nomor_polis:
        #     pytest.fail("Nomor polis tidak ditemukan di response!")
        # if not nomor_rekening:
        #     pytest.fail("Nomor Rekening tidak ditemukan di response!")

        # time.sleep(2)

        # ================= STEP 2: Verifikasi Database =================
        test_steps_rendered.append("[Test_Step_2]: Verifikasi database Covering Validation")
        screenshot_rendered.append(None)

        db_query, db_result = fetch_policy_by_no(nomor_rekening_pinjaman)
        

        if not db_result:
            pytest.fail(f"Data polis dengan nomor '{nomor_rekening_pinjaman}' tidak ditemukan di database!")
        else:
            print("[INFO] Data polis ditemukan di DB:")
            for k, v in db_result.items():
                print(f" - {k}: {v}")

        
        # ================= STEP 3: Verifikasi data DB dan Payload =================
        test_steps_rendered.append("[Test_Step_3]: Verifikasi data di Db dan Payload")
        screenshot_rendered.append(None)

        db_verification_result = verify_db_vs_payload(db_result, payload)

        #============================ STEP 4 : Verifikasi Database IJP===============
        test_steps_rendered.append("[Test_Step_4]: Verifikasi Database IJP")
        screenshot_rendered.append(None)

        db_query_step4, db_result_step4 = fetch_policy_by_norekijp(nomor_rekening_pinjaman)

        if not db_result_step4:
            pytest.fail(f"Data IJP dengan nomor '{nomor_rekening_pinjaman}' tidak ditemukan di database!")
        else:
            print("[INFO] Data IJP ditemukan di DB:")
            for row in db_result_step4:
                for k, v in row.items():
                    print(f" - {k}: {v}")
        # #========================= STEP : 5 Verifikasi IJP dan perhitungan-=======================
        # test_steps_rendered.append("[Test_Step_5]: Verifikasi data di Db dan rumus IJP")
        # screenshot_rendered.append(None)
        # db_verification_result_ijp = verify_db_vs_payload(db_result, )



        # ================= GENERATE PDF =================
        generate_pdf_report(
            status="Passed",
            testcase_id= testcase_id,
            testcase_name=testcase_name,
            tester=tester_name,
            screenshot_rendered=screenshot_rendered,
            test_steps_rendered=test_steps_rendered,
            screenshot_paths=screenshot_rendered,
            actual_result=actual_result,
            payload=payload,
            response=response_json,
            payload_step_index=0,
            db_data=db_result,
            db_query=db_query,
            db_step_index=1,
            db_verification_step_index=2,
            nomor_rekening_pinjaman=nomor_rekening_pinjaman,
            db_verification_result=db_verification_result,
            db_query_step4 = db_query_step4,
            db_result_step4 = db_result_step4,
            db_step_index_step4=3

        )

        assert True

    except Exception as e:
        import traceback, sys
        failed_step_index = len(test_steps_rendered) - 1
        tb = traceback.extract_tb(sys.exc_info()[2])[0]
        line_number = tb.lineno
        file_name = tb.filename
        function_name = tb.name
        error_type = type(e).__name__
        error_detail = str(e).strip() or "Tidak ada detail error"
        error_message = f"{error_type} | Baris: {line_number} | Detail: {error_detail}"

        screenshot_path_fail = save_screenshot(driver, base_name="screenshot_gagal", testcase_id=testcase_id, testcase_name=testcase_name)
        # Jika pakai Selenium driver, bisa save screenshot
        # screenshot_path_fail = save_screenshot(driver, base_name="screenshot_gagal", testcase_id="TC03", testcase_name="Output FAD1 Customs Bond")

        generate_pdf_report(
            status="Not Passed",
            testcase_id= testcase_id,
            testcase_name=testcase_name,
            tester=tester_name,
            screenshot_rendered=screenshot_rendered,
            test_steps_rendered=test_steps_rendered,
            screenshot_paths=screenshot_rendered + [screenshot_path_fail],
            actual_result=error_message,
            failed_step_index=failed_step_index,
            payload=payload,
            response=response_json,
            payload_step_index=0,
            db_data=db_result,
            db_query=db_query,
            db_step_index=1,
            db_verification_step_index=2,
            nomor_rekening_pinjaman=nomor_rekening_pinjaman,
            db_verification_result=db_verification_result,
            db_query_step4 = db_query_step4,
            db_result_step4 = db_result_step4,
            db_step_index_step4=3

        )

        traceback.print_exc()
        assert False, error_message
        