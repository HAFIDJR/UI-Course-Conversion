import streamlit as st
import pandas as pd

# Custom CSS for modern green theme with beautiful table designs
st.markdown(
    """
    <style>
        /* General styling */
        body {
            background-color: #f0f7f4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-container {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 100, 0, 0.08);
            margin: 1rem;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
            min-height: 400px;
        }
        h1 {
            color: #2e7d32;
            font-size: 2.2rem;
            margin-bottom: 1rem;
            text-align: center;
        }
        h2, h3 {
            color: #2e7d32;
            font-size: 1.5rem;
        }
        p {
            color: #4a4a4a;
            font-size: 1.1rem;
        }

        /* Input section styling */
        .input-section {
            background-color: #f9fcf9;
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px solid #c8e6c9;
            margin: 1.5rem 0;
        }

        /* Radio button styling */
        .stRadio > label {
            color: #2e7d32;
            font-weight: 500;
            font-size: 1.1rem;
            padding: 0.5rem;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stRadio > label:hover {
            background-color: #c8e6c9;
        }

        /* Text area and file uploader styling */
        .stTextArea textarea, .stFileUploader {
            border: 2px solid #c8e6c9;
            border-radius: 8px;
            background-color: #ffffff;
            transition: border-color 0.3s ease;
        }
        .stTextArea textarea:focus, .stFileUploader:hover {
            border-color: #2e7d32;
        }

        /* Button styling */
        .stButton>button {
            background-color: #2e7d32;
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #1b5e20;
            transform: translateY(-2px);
        }

        /* Success and warning messages */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
            font-size: 1rem;
        }

        /* TABLE STYLING - ENHANCED */
        .dataframe {
            border: none !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 20px rgba(0, 100, 0, 0.15) !important;
            font-family: 'Segoe UI', sans-serif !important;
        }
        
        .dataframe thead tr {
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%) !important;
        }
        
        .dataframe thead th {
            color: white !important;
            font-weight: 600 !important;
            padding: 15px 20px !important;
            text-align: left !important;
            border: none !important;
            font-size: 1rem !important;
        }
        
        .dataframe tbody td {
            padding: 15px 20px !important;
            border-bottom: 1px solid #e8f5e9 !important;
            color: #424242 !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #f9fcf9 !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: #e8f5e9 !important;
            transform: scale(1.01) !important;
            transition: all 0.2s ease !important;
        }

        /* Result Cards Styling */
        .result-section {
            background: linear-gradient(135deg, #f9fcf9 0%, #ffffff 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #c8e6c9;
            margin: 2rem 0;
            box-shadow: 0 6px 25px rgba(0, 100, 0, 0.1);
        }

        .result-header {
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-size: 1.3rem;
            font-weight: 600;
        }

        /* Metric Cards */
        .metric-row {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 100, 0, 0.1);
            border-top: 4px solid #4caf50;
            fle
            width:full;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 100, 0, 0.2);
        }

        .metric-number {
            font-size: 2rem;
            font-weight: bold;
            color: #2e7d32;
            margin-bottom: 0.5rem;
        }

        .metric-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Download Button Special Styling */
        .download-section {
            text-align: center;
            margin: 2rem 0;
            padding: 1.5rem;
            background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
            border-radius: 12px;
            border: 2px dashed #4caf50;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .main-container, .result-section {
            animation: fadeIn 0.6s ease-in;
        }

        /* Hide sidebar completely */
        .css-1lcbmhc.e1fqkh3o0 {
            display: none;
        }
        .css-1d391kg.e1fqkh3o1 {
            padding-left: 1rem;
        }

        /* Status Badge */
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .status-wajib {
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef5350;
        }
        .status-pilihan {
            background: #e3f2fd;
            color: #1565c0;
            border: 1px solid #42a5f5;
        }
        .status-praktek {
            background: #f3e5f5;
            color: #7b1fa2;
            border: 1px solid #ab47bc;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize session state for form submissions
if "text_submitted" not in st.session_state:
    st.session_state.text_submitted = False
if "file_submitted" not in st.session_state:
    st.session_state.file_submitted = False
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# Hasil dari Konversi Akan Ditampilkan Disini
def create_sample_results():
    """Create sample data for demonstration"""
    sample_data = {
        "Kode MK": ["CS101", "CS102", "CS201", "CS202", "CS301"],
        "Nama Mata Kuliah": [
            "Algoritma dan Pemrograman I",
            "Matematika Diskrit",
            "Struktur Data",
            "Basis Data",
            "Rekayasa Perangkat Lunak",
        ],
        "SKS": [3, 3, 3, 3, 4],
        "Semester": [1, 1, 2, 2, 3],
        "Deskripsi": [
            "Pengenalan konsep algoritma dan pemrograman dasar",
            "Konsep matematika diskrit untuk ilmu komputer",
            "Implementasi struktur data dalam pemrograman",
            "Desain dan implementasi basis data",
            "Metodologi pengembangan perangkat lunak",
        ],
    }
    return pd.DataFrame(sample_data)


def display_conversion_results():
    """Display beautiful conversion results with tables and metrics"""
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown(
        '<div class="result-header">📊 Hasil Konversi Silabus</div>',
        unsafe_allow_html=True,
    )

    # Create sample data
    df = create_sample_results()

    # Display metrics
    col1, col2, col3 = st.columns(3)
    jumlah_matakuliah = 15

    with col1:
        st.markdown(
            f"""
    <div class="metric-card">
        <div class="metric-number">{3}</div>
        <div class="metric-label">Total Mata Kuliah</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-number">16</div>
            <div class="metric-label">Total SKS</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="metric-card">
            <div class="metric-number">3</div>
            <div class="metric-label">Semester</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Display main conversion table
    st.subheader("📋 Tabel Konversi Mata Kuliah")

    # Display the main table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nama Mata Kuliah": st.column_config.TextColumn(
                "Nama Mata Kuliah", width="large"
            ),
            "SKS": st.column_config.NumberColumn("SKS", width="small"),
            "Semester": st.column_config.NumberColumn("Semester", width="small"),
            "Deskripsi": st.column_config.TextColumn("Deskripsi", width="large"),
        },
    )
    # Download section
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.markdown("### 💾 **Unduh Hasil Konversi**")
    st.markdown(
        "Klik tombol di bawah untuk mengunduh hasil konversi dalam format yang diinginkan:"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name="hasil_konversi_silabus.csv",
            mime="text/csv",
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Main app layout
st.title("🎓 Konversi Silabus Matakuliah 2025")
st.markdown("---")

# Input section in main content
st.subheader("📝 Pilih Mode Input")

# Mode selection
input_mode = st.radio(
    "Bagaimana Anda ingin memasukkan silabus?",
    ["📄 Deskripsi Teks", "📁 Unggah File"],
    index=0,
)

st.markdown("---")

# Form for text input
if input_mode == "📄 Deskripsi Teks":
    st.subheader("✍️ Masukkan Deskripsi Silabus")
    with st.form("form_text"):
        text_input = st.text_area(
            "Deskripsi Silabus:",
            height=200,
            placeholder="Contoh: Mata kuliah ini membahas tentang pemrograman dasar, algoritma, dan struktur data. Mahasiswa akan mempelajari konsep-konsep fundamental dalam pemrograman menggunakan bahasa Python...",
            help="Masukkan deskripsi lengkap silabus mata kuliah Anda",
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_text = st.form_submit_button("🚀 Konversi Deskripsi Teks")

        if submit_text:
            if text_input.strip():
                st.session_state.input_text = text_input
                st.session_state.text_submitted = True
                st.session_state.file_submitted = False
                st.session_state.uploaded_file = None
                st.rerun()
            else:
                st.error("⚠️ Harap masukkan deskripsi silabus terlebih dahulu!")

# Form for file upload
elif input_mode == "📁 Unggah File":
    st.subheader("📤 Unggah File Silabus")
    with st.form("form_file"):
        uploaded_file = st.file_uploader(
            "Pilih File Silabus:",
            type=["txt", "pdf", "docx"],
            help="Format yang didukung: .txt, .pdf, .docx (maksimal 200MB)",
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_file = st.form_submit_button("🚀 Konversi File")

        if submit_file:
            if uploaded_file is not None:
                st.session_state.uploaded_file = uploaded_file
                st.session_state.file_submitted = True
                st.session_state.text_submitted = False
                st.session_state.input_text = ""
                st.rerun()
            else:
                st.error("⚠️ Harap pilih file untuk diunggah!")

# Results section
st.markdown("---")

# Display results based on submission
if st.session_state.text_submitted and st.session_state.input_text:
    st.success("✅ Deskripsi berhasil diterima dan sedang diproses!")

    with st.expander("📋 Lihat Deskripsi yang Dimasukkan", expanded=False):
        st.write(st.session_state.input_text)

    # Show conversion results
    display_conversion_results()

    # Add a reset button
    if st.button("🔄 Input Baru"):
        st.session_state.text_submitted = False
        st.session_state.input_text = ""
        st.rerun()

elif st.session_state.file_submitted and st.session_state.uploaded_file:
    st.success("✅ File berhasil diunggah dan sedang diproses!")

    with st.expander("📁 Detail File yang Diunggah", expanded=False):
        st.write(f"**Nama File:** {st.session_state.uploaded_file.name}")
        st.write(f"**Ukuran:** {st.session_state.uploaded_file.size} bytes")
        st.write(f"**Tipe:** {st.session_state.uploaded_file.type}")

    # Show conversion results
    display_conversion_results()

    # Add a reset button
    if st.button("🔄 Input Baru"):
        st.session_state.file_submitted = False
        st.session_state.uploaded_file = None
        st.rerun()

else:
    st.info(
        "👋 Selamat datang! Silakan pilih mode input di atas dan masukkan data silabus untuk memulai konversi."
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <small>🎓 Sistem Konversi Silabus Matakuliah 2025 | Dibuat dengan M HAFID NUR FIRMANSYAH ❤️</small>
    </div>
    """,
    unsafe_allow_html=True,
)
