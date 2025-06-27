import camelot
import pandas as pd

from cleanText import cleanText


def uploadFile(file):
    print("Mencoba ekstrak dengan Camelot...")

    # --- Step 1: Ekstraksi Lattice ---
    try:
        tables_lattice = camelot.read_pdf(file, pages="all", flavor="lattice")
        print(f"Tabel ditemukan (lattice): {len(tables_lattice)}")
    except Exception as e:
        print(f"❌ Error lattice: {e}")
        tables_lattice = []

    # --- Step 2: Ekstraksi Stream ---
    try:
        tables_stream = camelot.read_pdf(file, pages="all", flavor="stream")
        print(f"Tabel ditemukan (stream): {len(tables_stream)}")
    except Exception as e:
        print(f"❌ Error stream: {e}")
        tables_stream = []

    # --- Step 3: Gabungkan dan deduplikasi ---
    all_tables = list(tables_lattice) + list(tables_stream)

    unique_table_strings = set()
    unique_tables = []

    for table in all_tables:
        df = table.df
        if df.empty:
            continue

        df_clean = df.dropna(how="all").dropna(axis=1, how="all")
        table_str = df_clean.to_string()

        if table_str not in unique_table_strings:
            unique_table_strings.add(table_str)
            unique_tables.append(df)

    print(f"Total tabel unik: {len(unique_tables)}")

    # --- Step 4: Proses Tabel ---
    result = []
    for idx, table in enumerate(unique_tables, start=1):
        try:
            df = table.copy()
            df = df.dropna(how="all").dropna(axis=1, how="all")
            df.columns = [str(c) for c in df.columns]  # pastikan semua kolom string
            df = df.loc[:, ~df.columns.str.contains("^Unnamed", na=False)]
            df = df.drop_duplicates()

            if df.empty:
                continue

            df.columns = [str(c) for c in df.columns]
            rows = df.to_dict(orient="records")

            formatted_rows = []
            for row in rows:
                cleaned_row = []
                for key, value in row.items():
                    if pd.notna(value) and str(value).strip():
                        cleaned_key = key.strip()
                        cleaned_value = (
                            str(value).replace("\r", "").replace("\n", " ").strip()
                        )
                        cleaned_row.append(f"{cleaned_key}: {cleaned_value}")
                if cleaned_row:
                    formatted_rows.append(", ".join(cleaned_row))

            if formatted_rows:
                result.append(
                    {"tabel": f"Tabel {idx}", "isiTabel": " | ".join(formatted_rows)}
                )
                print(f"✅ Tabel {idx} berhasil diproses.")
            else:
                print(f"⚠️ Tabel {idx} kosong setelah formatting.")

        except Exception as e:
            print(f"❌ Gagal memproses tabel {idx}: {e}")

    semua_isi_tabel_strings = [
        item["isiTabel"] for item in result if item.get("isiTabel")
    ]

    # Gabungkan semua string isi tabel menjadi satu teks utuh
    teks_utuh_hasil_tabel = " ".join(semua_isi_tabel_strings)

    return cleanText(teks_utuh_hasil_tabel)
