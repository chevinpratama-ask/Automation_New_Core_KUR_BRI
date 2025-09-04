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
            fid_program AS "FIDProgram",
            plafon_pinjaman AS "Plafon",
            outstanding_pinjaman AS "Outstanding"
            
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
