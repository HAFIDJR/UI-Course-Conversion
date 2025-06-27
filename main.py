import streamlit as st
import pandas as pd
import hashlib
import json
from datetime import datetime
from conversionData import conversionData
from ConvetFileToText import uploadFile
from components import cssStreamlit


def get_row_hash(row):
    return hashlib.md5(json.dumps(row, sort_keys=True).encode()).hexdigest()


# Initialize session state
if "text_submitted" not in st.session_state:
    st.session_state.text_submitted = False
if "file_submitted" not in st.session_state:
    st.session_state.file_submitted = False
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "saved_recommendations" not in st.session_state:
    st.session_state.saved_recommendations = []
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1
if "selected_courses" not in st.session_state:
    st.session_state.selected_courses = []


cssStreamlit.css()


# CRUD Functions
def save_recommendation(
    nama_mahasiswa,
    nim,
    judul_silabus,
    semester,
    conversion_data,
    selected_mata_kuliah=None,
):
    """Save recommendation to session state"""
    # If specific mata kuliah are selected, filter the data
    if selected_mata_kuliah:
        filtered_data = conversion_data[
            conversion_data.index.isin(selected_mata_kuliah)
        ]
    else:
        filtered_data = conversion_data

    recommendation = {
        "id": len(st.session_state.saved_recommendations) + 1,
        "nama_mahasiswa": nama_mahasiswa,
        "nim": nim,
        "judul_silabus": judul_silabus,
        "semester": semester,
        "tanggal_dibuat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_konversi": filtered_data.to_dict("records"),
        "total_mata_kuliah": len(filtered_data),
        "total_sks": filtered_data["sks"].sum(),
        "is_selected": bool(
            selected_mata_kuliah
        ),  # Flag to indicate if specific courses were selected
    }
    st.session_state.saved_recommendations.append(recommendation)


def update_recommendation(index, nama_mahasiswa, nim, judul_silabus):
    """Update existing recommendation"""
    if 0 <= index < len(st.session_state.saved_recommendations):
        st.session_state.saved_recommendations[index]["nama_mahasiswa"] = nama_mahasiswa
        st.session_state.saved_recommendations[index]["nim"] = nim
        st.session_state.saved_recommendations[index]["judul_silabus"] = judul_silabus


def delete_recommendation(index):
    """Delete recommendation from session state"""
    if 0 <= index < len(st.session_state.saved_recommendations):
        st.session_state.saved_recommendations.pop(index)


def get_recommendations_df():
    """Convert saved recommendations to DataFrame for display"""
    if not st.session_state.saved_recommendations:
        return pd.DataFrame()

    data = []
    for rec in st.session_state.saved_recommendations:
        data.append(
            {
                "ID": rec["id"],
                "Nama Mahasiswa": rec["nama_mahasiswa"],
                "NIM": rec["nim"],
                "Judul Silabus": rec["judul_silabus"],
                "Semester": rec["semester"],
                "Total Mata Kuliah": rec["total_mata_kuliah"],
                "Total SKS": rec["total_sks"],
                "Tanggal Dibuat": rec["tanggal_dibuat"],
            }
        )
    return pd.DataFrame(data)


def display_conversion_results():
    """Display beautiful conversion results with tables and metrics"""
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown(
        '<div class="result-header">📊 Hasil Konversi Silabus</div>',
        unsafe_allow_html=True,
    )

    # Create sample data
    df = conversionData(st.session_state.input_text or st.session_state.input_text_file,st.session_state.judul_deskripsi_silabus)
    df = df[df["semester"] == st.session_state.semester]
    df = df.reset_index(drop=True)  # Reset index for easier selection
    total_mata_kuliah = len(df)
    total_sks = df["sks"].sum()

    # Display metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
    <div class="metric-card">
        <div class="metric-number">{total_mata_kuliah}</div>
        <div class="metric-label">Total Mata Kuliah</div>
    </div>
    """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-number">{total_sks}</div>
            <div class="metric-label">Total SKS</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-number">{st.session_state.semester}</div>
            <div class="metric-label">Semester</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Display main conversion table with selection
    st.subheader("📋 Tabel Konversi Mata Kuliah")

    # Add selection mode
    selection_mode = st.radio(
        "Mode Penyimpanan:",
        ["💾 Simpan Semua Mata Kuliah", "🎯 Pilih Mata Kuliah Tertentu"],
        index=0,
        help="Pilih apakah ingin menyimpan semua mata kuliah atau hanya yang dipilih",
    )

    if selection_mode == "🎯 Pilih Mata Kuliah Tertentu":
        st.markdown("##### ✅ Pilih mata kuliah yang ingin disimpan:")

        # Create checkboxes for each course
        for idx, row in df.iterrows():
            row_data = row.to_dict()
            row_hash = get_row_hash(row_data)
            checkbox_key = f"course_{row_hash}"

            col1, col2, col3 = st.columns([1, 4, 1])

            with col1:
                is_selected = st.checkbox(
                    "",
                    key=checkbox_key,
                    value=any(
                        get_row_hash(d) == row_hash
                        for d in st.session_state.selected_courses
                    ),
                )

                if is_selected and not any(
                    get_row_hash(d) == row_hash
                    for d in st.session_state.selected_courses
                ):
                    st.session_state.selected_courses.append(row_data)

                elif not is_selected:
                    st.session_state.selected_courses = [
                        d
                        for d in st.session_state.selected_courses
                        if get_row_hash(d) != row_hash
                    ]

            with col2:
                st.write(f"**{row['subject']}**")

            with col3:
                st.write(f"**{row['sks']} SKS**")

        # Show selected courses summary
        if st.session_state.selected_courses:

            # selected_df = df.iloc[st.session_state.selected_courses]
            selected_df = pd.DataFrame(st.session_state.selected_courses)
            selected_sks = selected_df["sks"].sum()

            st.markdown("---")
            st.markdown("##### 📊 Ringkasan Mata Kuliah Terpilih:")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Mata Kuliah Terpilih", len(st.session_state.selected_courses)
                )
            with col2:
                st.metric("Total SKS Terpilih", selected_sks)

            # Display selected courses table
            st.markdown("##### 📋 Mata Kuliah yang Dipilih:")
            st.dataframe(
                selected_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "subject": st.column_config.TextColumn(
                        "Nama Mata Kuliah", width="large"
                    ),
                    "sks": st.column_config.NumberColumn("SKS", width="small"),
                    "semester": st.column_config.NumberColumn(
                        "Semester", width="small"
                    ),
                    "deskripsi": st.column_config.TextColumn(
                        "Deskripsi", width="large"
                    ),
                },
            )
    else:
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "subject": st.column_config.TextColumn(
                    "Nama Mata Kuliah", width="large"
                ),
                "sks": st.column_config.NumberColumn("SKS", width="small"),
                "semester": st.column_config.NumberColumn("Semester", width="small"),
            },
        )

    # Save recommendation section
    st.markdown("---")
    st.markdown('<div class="crud-section">', unsafe_allow_html=True)
    st.subheader("💾 Simpan Rekomendasi")

    # Show warning if no courses selected in selection mode
    if (
        selection_mode == "🎯 Pilih Mata Kuliah Tertentu"
        and not st.session_state.selected_courses
    ):
        st.warning("⚠️ Pilih minimal satu mata kuliah untuk disimpan!")

    with st.form("save_recommendation_form"):
        col1, col2 = st.columns(2)
        with col1:
            nama_mahasiswa = st.text_input(
                "Nama Mahasiswa *", placeholder="Contoh: John Doe"
            )
            nim = st.text_input("NIM *", placeholder="Contoh: 12345678")
        with col2:
            judul_silabus = st.text_input(
                "Judul Silabus *", placeholder="Contoh: Silabus Teknik Informatika"
            )

        # Show what will be saved
        if (
            selection_mode == "🎯 Pilih Mata Kuliah Tertentu"
            and st.session_state.selected_courses
        ):
            st.info(
                f"📋 Akan menyimpan {len(st.session_state.selected_courses)} mata kuliah terpilih dengan total {selected_df['sks'].sum()} SKS"
            )
        elif selection_mode == "💾 Simpan Semua Mata Kuliah":
            st.info(
                f"📋 Akan menyimpan semua {total_mata_kuliah} mata kuliah dengan total {total_sks} SKS"
            )

        save_button = st.form_submit_button("💾 Simpan Rekomendasi")

        if save_button:
            if nama_mahasiswa and nim and judul_silabus:
                if selection_mode == "🎯 Pilih Mata Kuliah Tertentu":
                    if st.session_state.selected_courses:
                        save_recommendation(
                            nama_mahasiswa,
                            nim,
                            judul_silabus,
                            st.session_state.semester,
                            df,
                            st.session_state.selected_courses,
                        )
                        st.success(
                            f"✅ Rekomendasi berhasil disimpan dengan {len(st.session_state.selected_courses)} mata kuliah terpilih!"
                        )
                        st.rerun()
                    else:
                        st.error("⚠️ Pilih minimal satu mata kuliah untuk disimpan!")
                else:
                    save_recommendation(
                        nama_mahasiswa,
                        nim,
                        judul_silabus,
                        st.session_state.semester,
                        df,
                    )
                    st.success(
                        "✅ Rekomendasi berhasil disimpan dengan semua mata kuliah!"
                    )
                    st.rerun()
            else:
                st.error("⚠️ Harap isi semua field yang wajib!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Download section
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    st.markdown("### 💾 **Unduh Hasil Konversi**")
    st.markdown(
        "Klik tombol di bawah untuk mengunduh hasil konversi dalam format yang diinginkan:"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        # Download all courses
        csv_all = df.to_csv(index=False)
        st.download_button(
            label="📄 Download Semua (CSV)",
            data=csv_all,
            file_name="hasil_konversi_silabus_semua.csv",
            mime="text/csv",
        )

    with col2:
        # Download selected courses (if any)
        if (
            selection_mode == "🎯 Pilih Mata Kuliah Tertentu"
            and st.session_state.selected_courses
        ):
            csv_selected = selected_df.to_csv(index=False)
            st.download_button(
                label="📄 Download Terpilih (CSV)",
                data=csv_selected,
                file_name="hasil_konversi_silabus_terpilih.csv",
                mime="text/csv",
            )
        else:
            st.button(
                "📄 Download Terpilih (CSV)",
                disabled=True,
                help="Pilih mata kuliah terlebih dahulu",
            )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def display_saved_recommendations():
    """Display saved recommendations with CRUD operations"""
    st.markdown("---")
    st.subheader("📚 Rekomendasi Tersimpan")

    if not st.session_state.saved_recommendations:
        st.info("Belum ada rekomendasi yang tersimpan.")
        return

    # Display summary
    recommendations_df = get_recommendations_df()

    # Metrics for saved recommendations
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-number">{len(st.session_state.saved_recommendations)}</div>
            <div class="metric-label">Total Rekomendasi</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        total_all_sks = sum(
            [rec["total_sks"] for rec in st.session_state.saved_recommendations]
        )
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-number">{total_all_sks}</div>
            <div class="metric-label">Total SKS Semua</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        total_all_mk = sum(
            [rec["total_mata_kuliah"] for rec in st.session_state.saved_recommendations]
        )
        st.markdown(
            f"""
        <div class="metric-card">
            <div class="metric-number">{total_all_mk}</div>
            <div class="metric-label">Total Mata Kuliah</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Display table of saved recommendations
    st.markdown("### 📋 Daftar Rekomendasi")
    st.dataframe(
        recommendations_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Nama Mahasiswa": st.column_config.TextColumn(
                "Nama Mahasiswa", width="medium"
            ),
            "NIM": st.column_config.TextColumn("NIM", width="medium"),
            "Judul Silabus": st.column_config.TextColumn(
                "Judul Silabus", width="large"
            ),
            "Semester": st.column_config.NumberColumn("Semester", width="small"),
            "Total Mata Kuliah": st.column_config.NumberColumn(
                "Total MK", width="small"
            ),
            "Total SKS": st.column_config.NumberColumn("Total SKS", width="small"),
            "Tanggal Dibuat": st.column_config.TextColumn(
                "Tanggal Dibuat", width="medium"
            ),
        },
    )

    # CRUD Operations
    st.markdown("### ⚙️ Operasi Data")

    # Select recommendation for operations
    if st.session_state.saved_recommendations:
        selected_rec = st.selectbox(
            "Pilih Rekomendasi:",
            options=range(len(st.session_state.saved_recommendations)),
            format_func=lambda x: f"{st.session_state.saved_recommendations[x]['nama_mahasiswa']} - {st.session_state.saved_recommendations[x]['judul_silabus']}",
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("👁️ Lihat Detail"):
                show_detail_recommendation(selected_rec)

        with col2:
            if st.button("✏️ Edit"):
                st.session_state.edit_mode = True
                st.session_state.edit_index = selected_rec
                st.rerun()

        with col3:
            if st.button("🗑️ Hapus", key="delete_button"):
                delete_recommendation(selected_rec)
                st.success("✅ Rekomendasi berhasil dihapus!")
                st.rerun()

        with col4:
            if st.button("📄 Download PDF"):
                generate_pdf_report(selected_rec)

    # Edit form
    if st.session_state.edit_mode and st.session_state.edit_index >= 0:
        st.markdown("### ✏️ Edit Rekomendasi")
        rec = st.session_state.saved_recommendations[st.session_state.edit_index]

        with st.form("edit_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_nama = st.text_input("Nama Mahasiswa", value=rec["nama_mahasiswa"])
                new_nim = st.text_input("NIM", value=rec["nim"])
            with col2:
                new_judul = st.text_input("Judul Silabus", value=rec["judul_silabus"])

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Simpan Perubahan"):
                    update_recommendation(
                        st.session_state.edit_index, new_nama, new_nim, new_judul
                    )
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = -1
                    st.success("✅ Rekomendasi berhasil diupdate!")
                    st.rerun()

            with col2:
                if st.form_submit_button("❌ Batal"):
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = -1
                    st.rerun()

    # Download all recommendations
    st.markdown("### 📥 Download Semua Rekomendasi")
    if st.session_state.saved_recommendations:
        csv_all = recommendations_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Semua Rekomendasi (CSV)",
            data=csv_all,
            file_name=f"semua_rekomendasi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )


def show_detail_recommendation(index):
    """Show detailed view of a recommendation"""
    if 0 <= index < len(st.session_state.saved_recommendations):
        rec = st.session_state.saved_recommendations[index]

        st.markdown("### 📋 Detail Rekomendasi")

        # Student info card
        status_text = (
            "Mata Kuliah Terpilih"
            if rec.get("is_selected", False)
            else "Semua Mata Kuliah"
        )
        st.markdown(
            f"""
        <div class="student-info-card">
            <h4>👤 Informasi Mahasiswa</h4>
            <p><strong>Nama:</strong> {rec['nama_mahasiswa']}</p>
            <p><strong>NIM:</strong> {rec['nim']}</p>
            <p><strong>Judul Silabus:</strong> {rec['judul_silabus']}</p>
            <p><strong>Semester:</strong> {rec['semester']}</p>
            <p><strong>Jenis Simpan:</strong> {status_text}</p>
            <p><strong>Tanggal Dibuat:</strong> {rec['tanggal_dibuat']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Conversion data
        st.markdown("#### 📚 Data Konversi Mata Kuliah")
        conversion_df = pd.DataFrame(rec["data_konversi"])
        st.dataframe(conversion_df, use_container_width=True, hide_index=True)

        # Download individual recommendation
        csv_individual = conversion_df.to_csv(index=False)
        st.download_button(
            label=f"📄 Download Rekomendasi {rec['nama_mahasiswa']}",
            data=csv_individual,
            file_name=f"rekomendasi_{rec['nama_mahasiswa']}_{rec['nim']}.csv",
            mime="text/csv",
        )


def generate_pdf_report(index):
    """Generate PDF report for a recommendation"""
    # This is a placeholder - you would need to implement PDF generation
    # using libraries like reportlab or weasyprint
    st.info("🚧 Fitur PDF dalam pengembangan. Saat ini gunakan download CSV.")


# Main app layout
st.title("🎓 Konversi Silabus Matakuliah 2025")
st.markdown("---")

# Sidebar for navigation
st.sidebar.title("📋 Navigasi")
page = st.sidebar.selectbox(
    "Pilih Halaman:", ["🏠 Konversi Silabus", "📚 Rekomendasi Tersimpan"]
)

if page == "🏠 Konversi Silabus":
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

            judul_silabus = st.text_input(
                "Judul Deskripsi Silabus", placeholder="Pengembangan Website"
            )

            semester = st.number_input(
                "Semester Mahasiswa:", min_value=1, max_value=14, step=1
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_text = st.form_submit_button("🚀 Konversi Deskripsi Teks")

            if submit_text:
                if text_input.strip() and judul_silabus.strip():
                    st.session_state.input_text = text_input
                    st.session_state.selected_courses_temp = (
                        st.session_state.selected_courses
                    )
                    st.session_state.text_submitted = True
                    st.session_state.file_submitted = False
                    st.session_state.uploaded_file = None
                    st.session_state.semester = semester
                    st.session_state.judul_deskripsi_silabus = judul_silabus
                    st.session_state.input_text_file = ""
                    st.rerun()
                else:
                    st.error(
                        "⚠️ Harap masukkan deskripsi silabus atau Judul  Deksripsi Silabus terlebih dahulu!"
                    )

    # Form for file upload
    elif input_mode == "📁 Unggah File":
        st.subheader("📤 Unggah File Silabus")
        with st.form("form_file"):
            uploaded_file = st.file_uploader(
                "Pilih File Silabus:",
                type=["txt", "pdf", "docx"],
                help="Format yang didukung: .txt, .pdf, .docx (maksimal 200MB)",
            )
            semester = st.number_input(
                "Semester Mahasiswa:", min_value=1, max_value=14, step=1
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_file = st.form_submit_button("🚀 Konversi File Silabus")

            if submit_file:
                if uploaded_file is not None:
                    st.session_state.uploaded_file = uploaded_file
                    st.session_state.file_submitted = True
                    st.session_state.text_submitted = False
                    st.session_state.input_text = ""
                    st.session_state.semester = semester
                    # function to Upload File
                    data = uploadFile(uploaded_file)
                    print(data)
                    st.session_state.input_text_file = data
                    st.rerun()
                else:
                    st.error("⚠️ Harap pilih file untuk diunggah!")

    # Results section
    st.markdown("---")

    # Display results based on submission
    if st.session_state.text_submitted and st.session_state.input_text:
        st.success("✅ Deskripsi berhasil diterima")
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

elif page == "📚 Rekomendasi Tersimpan":
    display_saved_recommendations()

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
