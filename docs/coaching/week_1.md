### **2. Identifikasi Bagian yang Diucapkan oleh Dosen**
Dosen (Perempuan) aktif berbicara pada menit:
*   **00:00 - 00:01** (Menanyakan fungsi fitur kebijakan bank sentral).
*   **00:09 - 00:11** (Mengonfirmasi penjelasan kebijakan bank sentral).
*   **00:27 - 00:29** (Mengonfirmasi penjelasan fitur *hedging*).
*   **00:41 - 00:43** (Mengonfirmasi penjelasan alokasi portofolio).
*   **00:54 - 00:57** (Menanyakan kelanjutan penjelasan fitur).
*   **01:17 - 01:34** (Menanyakan detail rekomendasi keputusan portofolio: *buy*, *hold*, atau *sell*).
*   **01:45 - 02:00** (Meminta demo dijalankan kembali dan menyarankan mencoba saham Indonesia seperti BBRI).
*   **02:22 - 03:00** (Mengkritisi batasan sistem yang ternyata hanya mendukung pasar saham US, serta mempertanyakan relevansi analisis makro dan sumber berita yang digunakan).
*   **03:04 - 03:08** (Meminta dicoba analisis saham Nvidia).
*   **03:11 - 03:15** (Menanyakan status rekomendasi Nvidia).
*   **03:21 - 03:24** (Mengonfirmasi target jangka waktu prediksi 3 bulan).
*   **03:36 - 03:55** (Menanyakan ketersediaan opsi rekomendasi *buy* dan menganalisis implikasi rekomendasi *hold* dan *sell* yang mengasumsikan pengguna sudah memiliki saham).
*   **03:59 - 04:45** (Memberikan evaluasi akhir mengenai status prediksi jangka waktu 3 bulan agar dibuat lebih dinamis, serta perlunya penyesuaian terhadap volatilitas masing-masing saham).

---

### **3. Pengumpulan Penjelasan Penting Dosen terkait Project**
Dalam diskusi tersebut, dosen menggarisbawahi beberapa kelemahan fundamental dan memberikan arahan pengembangan sistem analisis saham yang sedang dibuat mahasiswa:
*   **Relevansi Data Makro dan Berita:** Mahasiswa harus memastikan berita dan analisis makroekonomi yang ditarik oleh sistem relevan dengan pasar saham yang didukung (dalam hal ini, pasar saham US/USD).
*   **Karakteristik Pasar Saham US:** Analisis variabel makroekonomi untuk pasar global (USD) jauh lebih kompleks daripada pasar lokal (Indonesia) dan membutuhkan penyesuaian indikator yang tepat.
*   **Sifat Prediksi Jangka Waktu (*Timeframe*):** Target jangka waktu prediksi yang saat ini di-*set* pada 3 bulan harus dipastikan bersifat dinamis (tidak statis atau sekadar nilai *default*).
*   **Faktor Volatilitas Saham:** Setiap saham memiliki tingkat volatilitas yang berbeda. Rekomendasi investasi jangka waktu tertentu (misal: 3 bulanan) tidak bisa digeneralisasi untuk semua jenis saham, terutama untuk saham-saham yang sangat volatil.

---

### **4. Rangkuman Penjelasan Dosen (Poin-Poin Detail & Terstruktur)**

*   **Validasi Pasar Saham dan Sumber Data:**
    *   Sistem saat ini baru mendukung (*support*) saham luar negeri berbasis USD (contoh: Apple, Nvidia) dan belum mendukung saham Indonesia (seperti BBRI).
    *   Mahasiswa harus memastikan sinkronisasi antara berita yang ditarik oleh sistem dengan jenis pasar saham yang dianalisis. Jika fokus pada saham USD, maka data makroekonomi dan berita yang digunakan harus yang mempengaruhi pasar keuangan Amerika Serikat/global.

*   **Evaluasi Logika Rekomendasi Portofolio (*Decision Making*):**
    *   Sistem harus membedakan dengan jelas logika di balik rekomendasi *Buy*, *Hold*, dan *Sell*. 
    *   Rekomendasi *Hold* dan *Sell* secara logis mengasumsikan bahwa pengguna sudah memiliki (*own*) aset saham tersebut. Dosen menekankan pentingnya kehadiran opsi *Buy* sebagai rekomendasi utama bagi pengguna yang belum memiliki aset.

*   **Dinamisasi Jangka Waktu Prediksi (*Prediction Timeframe*):**
    *   Prediksi target investasi (saat ini diset selama 3 bulan) dikritisi agar tidak bersifat statis/angka mati (*default*). 
    *   Sistem perlu dikembangkan agar jangka waktu prediksi ini bisa menyesuaikan secara dinamis berdasarkan input pengguna atau algoritma pendukung.

*   **Segmentasi Saham Berdasarkan Volatilitas:**
    *   Tidak semua saham cocok dianalisis atau diprediksi menggunakan kerangka waktu 3 bulanan.
    *   Untuk saham dengan volatilitas yang sangat tinggi (sangat volatil), jangka waktu 3 bulan mungkin kurang relevan. Mahasiswa disarankan untuk memetakan atau mengelompokkan saham-saham mana saja yang memang cocok untuk dianalisis dalam jangka waktu menengah (3 bulanan) tersebut.