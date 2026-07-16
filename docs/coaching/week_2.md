### **2. Bagian yang Diucapkan oleh Dosen**
Dosen aktif memberikan tanggapan, kritik, dan arahan pada menit-menit berikut:
* **00:17 - 00:18** (Menanyakan pasar saham yang didukung).
* **00:22 - 00:23** (Mengonfirmasi opsi saham Indonesia).
* **00:34 - 00:35** (Meminta kelanjutan penjelasan).
* **00:44 - 00:46** (Menanyakan detail kode emiten/JK).
* **00:54 - 01:17** (Mengkritisi asal-usul data *target position*, *sizing*, *confidence level* dari EA, serta mempertanyakan validitasnya).
* **01:17 - 02:00** (Menekankan pentingnya kontrol logika di balik keputusan rekomendasi investasi agar tidak terlihat acak/random).
* **02:01 - 02:14** (Menanyakan kriteria spesifik rekomendasi *hold* dan komunikasinya antar *agent*).
* **02:14 - 02:30** (Mengejar kejelasan indikator *technical analysis* yang menghasilkan status *bullish*/*bearish*).
* **02:44 - 02:51** (Menemukan kejanggalan logika: tren *bearish* namun rekomendasi yang keluar tetap *hold*).
* **02:52 - 03:41** (Meminta mahasiswa merancang opsi keputusan investasi yang logis serta memperjelas cara membaca *dashboard*).
* **03:48 - 03:59** (Mengkritisi ketidakcocokan profil pengguna: sistem menyarankan *hold* kepada pengguna yang belum memiliki saham tersebut).
* **04:18 - 04:29** (Mempertanyakan mengapa logika penanganan profil pengguna tersebut hanya ada di *back-end*/*report* dan belum diintegrasikan ke *front-end*/*dashboard*).
* **04:30 - 05:56** (Memberikan arahan komprehensif terkait perbaikan UI/UX bagi pengguna baru, pentingnya deskripsi/panduan awal, kejelasan input data, dan penetapan nilai *default* yang intuitif).
* **05:57 - 06:18** (Menanyakan detail teknis konsumsi token LLM dan mekanisme pencegahan *rate limit*).
* **06:19 - 06:34** (Merespons taktik penyediaan multi-akun API secara humoris).
* **06:35 - 06:51** (Menanyakan dan mengonfirmasi rencana *hosting* menggunakan VPS *dedicated*).
* **06:52 - 07:11** (Evaluasi akhir berupa saran penyempurnaan UI/UX dan menutup sesi diskusi).

---

### **3. Pengumpulan Penjelasan Penting Dosen terkait Project**
Dalam diskusi ini, dosen mengidentifikasi beberapa kelemahan kritis pada sistem analisis saham mahasiswa, terutama pada aspek **Logika Pengambilan Keputusan (Decision Making Logic)** dan **Pengalaman Pengguna (UI/UX)**. 

Dosen menekankan bahwa sistem tidak boleh hanya menampilkan data dari EA (Expert Advisor) atau AI secara mentah, melainkan harus memiliki dasar logika yang valid, terkontrol, konsisten, dan dapat dipertanggungjawabkan secara finansial.

---

### **4. Rangkuman Penjelasan Dosen (Poin-Poin Detail & Terstruktur)**

#### **A. Validasi Logika Pengambilan Keputusan (*Decision Making*)**
* **Kejelasan Alasan (*Reasoning*) Rekomendasi:** Mahasiswa harus tahu persis dasar analisis (baik *technical* maupun aspek lainnya) yang digunakan oleh AI/EA untuk memunculkan rekomendasi (*Buy, Hold, Sell*). Logika ini harus sepenuhnya dikontrol oleh sistem pengembang, bukan dibiarkan acak (*random*).
* **Sinkronisasi Indikator dan Output:** Dosen menemukan anomali di mana indikator menunjukkan pasar sedang *bearish* (tekanan jual), namun sistem tetap merekomendasikan *hold*. Mahasiswa diinstruksikan untuk menyelaraskan kondisi pasar dengan output rekomendasi secara logis.
* **Relevansi Berdasarkan Profil Portofolio Pengguna:** 
  * Rekomendasi **Hold** dan **Sell** secara logis hanya berlaku bagi pengguna yang **sudah memiliki** (*own*) saham tersebut di portofolionya. 
  * Bagi pengguna baru yang belum memiliki saham tersebut, sistem harus memberikan rekomendasi alternatif seperti **Buy**, **Wait**, atau **Do Not Buy**. Perbedaan logika ini harus segera diimplementasikan pada tampilan *front-end*/*dashboard*, bukan hanya tertahan di laporan *back-end*.

#### **B. Perbaikan Desain Antarmuka dan Pengalaman Pengguna (UI/UX)**
* **Kemudahan untuk Pengguna Baru (*Onboarding Process*):** *Dashboard* saat ini dinilai terlalu membingungkan bagi pengguna baru karena langsung menyajikan data penuh tanpa panduan.
* **Panduan Penggunaan (*User Guide*):** Sistem perlu ditambahkan deskripsi singkat di halaman awal yang menjelaskan fungsi aplikasi, input apa saja yang harus dimasukkan pengguna, ke mana harus menginputnya, serta cara membaca visualisasi *dashboard*.
* **Penentuan Tampilan Utama (*Default View*):** Saat pertama kali dibuka tanpa pencarian spesifik, sistem harus menampilkan data *default* yang terstruktur, misalnya saham-saham paling populer yang sering dicari (*most searched stocks*) atau berdasarkan referensi pasar yang valid.
* **Lokalisasi Mata Uang:** Karena proyek telah diperluas untuk mendukung saham Indonesia (seperti BBRI, GOTO, BUMI), sistem harus mampu mengonversi satuan mata uang ke Rupiah (IDR) secara dinamis di bagian *front-end*, bukan tetap menggunakan Dolar (USD).

#### **C. Pengelolaan Sumber Daya API LLM**
* **Manajemen Token Gemini:** Dosen memastikan kesiapan sistem terhadap risiko *rate limit* saat mengonsumsi LLM API. Mahasiswa merancang solusi *roll-over* otomatis menggunakan sistem multi-akun API (saat ini menggunakan 3 akun) yang dikonfigurasi melalui file `.env`.

#### **D. Infrastruktur dan Deployment**
* **Hosting Dedicated:** Sistem dipastikan akan di-deploy menggunakan VPS (Virtual Private Server) *dedicated* milik mahasiswa guna menjamin performa dan stabilitas aplikasi saat dijalankan.