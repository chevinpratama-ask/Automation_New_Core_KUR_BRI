import pyodbc

def get_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=10.100.20.87;"
        "Database=DBMIGAOSKUR;"
        "UID=migrasi.aos;"
        "PWD=Askrindo%1234;"
    )

def fetch_policy_by_no(no_rekening_pinjaman):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT
            request_id AS "RequestID",
            f_id_program AS "FIDProgram",
            nama_program AS "NamaProgram",
            f_id_kategori_asuransi AS "FIDKategoriAsuransi",
            f_id_kategori_asuransi AS "FIDJenisAsuransi",
            no_rekening_pinjaman AS "NomorRekeningPinjaman",
            cif_rekening_simpanan AS "CIFRekeningPinjaman",
            LoanType AS "loan_type",
            loan_type_desc AS "LoanTypeDesc",
            jangka_waktu_bulan AS "JangkaWaktuBulan",
            jangka_waktu_plihan  AS "JangkaWaktuPilihan",
            suku_bunga_pinjaman AS "SukuBungaPinjamanTahun",
            plafon AS "Plafon",
            outstanding AS "Outstanding",
            total_eksposure AS "TotalEksposure",
            flag_corona AS "FlagCorona",
            flag_restruk AS "FlagRestruk",
            Kolektabilitas AS "Kolektabilitas",
            tanggal_akad_restruk AS "TanggalAkadKreditRestruk",
            tanggal_kredit_restruk AS "TanggalKreditRestruk",
            tanggal_akad_kredit AS "TanggalAkadKredit",
            tanggal_realisasi AS "TanggalRealisasi",
            tanggal_akhir_covering AS "TanggalJatuhTempo",
            tanggal_pembentukan_rekening AS "TanggalPembentukanRekening",
            unit_code AS "UnitCode",
            unit_desc AS "UnitDesc",
            branch_code AS "BranchCode",
            branch_desc AS "BranchDesc",
            region_code AS "RegionCode",
            region_desc AS "RegionDesc",
            maker_branch AS "MakerBranch",
            nomor_pk AS "NomorPerjanjianKredit",
            nilai_likuiditas AS "NilaiLikuiditas",
            sektor_ekonomi AS "SektorEkonomi",
            f_id_kategori_jenis_fasilitas AS "FIDKategoriJenisFasilitas",
            nama_peserta  AS "NamaPeserta",
            nomor_identitas AS "NomorIdentitas",
            npwp AS "NPWP",
            email AS "Email",
            tanggal_lahir AS "TanggalLahir",
            tempat_lahir AS "TempatLahir",
            f_id_jenis_kelamin AS "FIDJenisKelamin",
            jenis_kelamin AS "JenisKelamin",
            f_id_pendidikan AS "FIDPendidikan",
            pendidikan AS "Pendidikan",
            f_id_pekerjaan AS "FIDPekerjaan",
            pekerjaan AS "Pekerjaan",
            f_id_status_pernikahan AS "FIDStatusPernikahan",
            status_pernikahan AS "StatusPernikahan",
            nomor_hp AS "NomorHP",
            alamat1 AS "Alamat1",
            alamat2 AS "Alamat2",
            alamat3 AS "Alamat3",
            alamat4 AS "Alamat4",
            kode_pos AS "KodePos",
            kode_kabupaten_kota AS "KodeKabupatenKota",
            nama_perusahaan_inti AS "NamaPerusahaanInti",
            tanggal_mulai_usaha AS "TanggalMulaiUsaha",
            nomor_ijin_usaha AS "NomorIjinUsaha",
            modal_usaha AS "ModalUsaha",
            alamat_usaha AS "AlamatUsaha",
            jumlah_tenaga_kerja AS "JumlahTenagaKerja",
            nomor_rekening_pinjaman_sebelumnya  AS "NomorRekeningPinjamanSebelumnya",
            no_peserta_sebelumnya AS "NomorPesertaSebelumnya",
            nominal_premi_sebelumnya AS "NominalPremiSebelumnya",
            f_id_jenis_agunan AS "FIDJenisAgunan",
            f_id_agunan AS "FIDAgunan",
            
            -- Tambahkan alias lain sesuai field payload kamu
        FROM brisurf.t_covering_validation
        WHERE no_rekening_pinjaman = ?
    """
    cursor.execute(query, (no_rekening_pinjaman.strip(),))
    row = cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    conn.close()

    if row:
        return dict(zip(columns, row))  # ✅ Output: dict dengan key sesuai payload
    return {}
