# SHF (`Stock Hedge Fund`) Multi-Agent Quantitative Engine

Platform riset investasi dan analisis kuantitatif saham kelas institusi (*Institutional-Grade Autonomous AI Hedge Fund Engine*) berbasis arsitektur **True Multi-Agent** menggunakan **Python 3.13**, **FastAPI**, **LangGraph (`StateGraph`)**, **Google Gemini 3.1 Flash-Lite**, **Machine Learning Ensembles (`LightGBM` & `XGBoost`)**, dan komputasi matematis deterministik.

Sistem ini didesain khusus sebagai mesin pemroses kuantitatif *backend* murni (*Pure Backend Multi-Agent Architecture*) untuk mengeksekusi alur kerja analisis finansial secara mendalam, modular, dan asinkron tanpa ketergantungan pada lapisan antarmuka grafis (*No Frontend Included*).

---

## 🎯 Tujuan Utama & Kasus Penggunaan (*Use Case*)

1. **Pengambilan Keputusan Investasi Bebas Bias Emosional**: Menggantikan intuisi subjektif retail dengan pendekatan ilmiah kuantitatif kelas institusi yang memadukan analisis harga historis, indikator teknikal matematis, makroekonomi, aliran opsi (*options flow*), sentimen berita katalis, dan prediksi model *Machine Learning*.
2. **Penghapusan Halusinasi Matematis LLM (*Zero Math Hallucination*)**: Seluruh kalkulasi indikator teknikal (`MACD`, `RSI`, `Bollinger Bands`, `Ichimoku Cloud`) serta metrik risiko historis (`Sharpe Ratio`, `Sortino Ratio`, `CAGR`, `Max Drawdown`, `Value-at-Risk`) dihitung 100% menggunakan formula numerik deterministik (`pandas`, `numpy`, `scikit-learn`). **Google Gemini 3.1 Flash-Lite** difokuskan secara khusus untuk penalaran kontekstual, sintesis fundamental, analisis kebijakan makro, dan artikulasi tesis investasi (*Chief Investment Officer Articulation*).
3. **Audit Kuantitatif Multi-Tahun (*Long-Term Regime & Seasonality Audit*)**: Mampu menganalisis rentang data harian hingga 5 tahun (1.260+ bar trading) untuk menghitung rata-rata pertumbuhan tahunan (`CAGR 1Y/3Y/5Y`), klasifikasi rezim volatilitas, dan *Monthly Seasonality Heatmap* (probabilitas retur per bulan).
4. **Eksekusi Asinkron & Skalabilitas Tinggi (*High Concurrency & Fault Tolerance*)**: D dibangun di atas *event loop* asinkron (`AsyncIO`, `Celery`, `Redis`) dengan mekanisme validasi ketat menggunakan **Pydantic v2** dan penyimpanan *state* persisten di **MongoDB** (*Motor Async Driver*).

---

## 🏗️ Arsitektur Multi-Agent Terdesentralisasi (*Decentralized Multi-Agent Architecture*)

Sistem ini tidak menggunakan pendekatan *Centralized Orchestrator* tradisional yang rapuh (di mana satu node pengatur memonopoli seluruh keputusan dan menjadi titik kegagalan tunggal / *single point of failure*). Sebaliknya, **SHF** menerapkan **Arsitektur Multi-Agent Terdesentralisasi (*Decentralized & Peer-Verified Multi-Agent Network*)** di atas framework **LangGraph (`StateGraph`)**.

Dalam model terdesentralisasi ini, **10 Agen Kuantitatif Spesialistik** dikelompokkan ke dalam 4 lapisan otonom (*Autonomous Specialist Pods*) yang beroperasi secara sejajar (*parallel*) dan saling memverifikasi data di dalam *shared graph memory* (`HedgeFundState` berbasis **Pydantic v2**):

```
       [ REST API POST /api/v1/analyze | WebSocket /api/v1/ws/live ]
                                    │
                                    ▼
         [ FastAPI Asynchronous Engine (Uvicorn / Python 3.13) ]
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🌐 LAYER 1: DECENTRALIZED DATA & REGIME INGESTION POD                       │
│  ┌───────────────────────────────┐   ┌───────────────────────────────────┐  │
│  │   Market Data Agent           │   │ Quantitative Historical Regime    │  │
│  │  (Spot, Fundamental, OHLCV)   │   │  (5Y CAGR, Sharpe, Sortino, DD)   │  │
│  └───────────────┬───────────────┘   └─────────────────┬─────────────────┘  │
└──────────────────┼─────────────────────────────────────┼────────────────────┘
                   │  (Stateful Decentralized Hand-off)  │
                   ▼                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🧠 LAYER 2: DECENTRALIZED SPECIALIST ANALYSIS & INTELLIGENCE POD            │
│  ┌────────────────────────┐  ┌────────────────────────┐                     │
│  │ Technical Analysis     │  │ News Intelligence      │                     │
│  │ (11 Deterministic Math)│  │ (Gemini 3.1 Flash-Lite)│                     │
│  └───────────┬────────────┘  └───────────┬────────────┘                     │
│              │                           │                                  │
│  ┌───────────▼────────────┐  ┌───────────▼────────────┐                     │
│  │ Macro Economy Agent    │  │ Options Flow Agent     │                     │
│  │ (Fed Rate, Yield, CPI) │  │ (Put/Call Wall, Gamma) │                     │
│  └───────────┬────────────┘  └───────────┬────────────┘                     │
└──────────────┼───────────────────────────┼──────────────────────────────────┘
               │  (Parallel Multi-Domain Confluence Signals)                  │
               ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ LAYER 3: DECENTRALIZED RISK AUDIT & PREDICTIVE ENSEMBLE POD              │
│  ┌───────────────────────────────┐   ┌───────────────────────────────────┐  │
│  │ ML Prediction Agent           │   │ Quantitative Risk Manager Agent   │  │
│  │ (LightGBM, XGBoost Ensemble)  │   │ (Kelly Sizing, Stop-Loss Limits)  │  │
│  └───────────────┬───────────────┘   └─────────────────┬─────────────────┘  │
└──────────────────┼─────────────────────────────────────┼────────────────────┘
                   │  (Verified Quantitative Risk Budget & ML Target)         │
                   ▼                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚖️ LAYER 4: DECENTRALIZED CONSENSUS & MANDATE EXECUTION POD                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Portfolio Manager Agent (CIO Master Confluence & Mandate Articulation)│  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ Execution Agent (Institutional VWAP/TWAP Checklist & Iceberg Splitting)│  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
 [ MongoDB Async Motor Storage ] ─── [ Redis Distributed Pub/Sub & Cache ]
```

### Keunggulan Arsitektur Terdesentralisasi (*Why Decentralized Architecture?*)
* **Kemandirian Domain (*Domain-Specific Autonomy*)**: Agen *Technical Analysis* dapat mengevaluasi 11 indikator kuantitatif deterministik secara independen tanpa menunggu hasil *scraping* berita dari *News Intelligence Agent* atau komputasi *Options Flow*.
* **Cross-Verification & Zero Bias**: *ML Prediction Agent* dan *Risk Manager Agent* secara terdesentralisasi membandingkan sinyal *bullish/bearish* dari agen lain. Jika *News Agent* sangat *bullish* namun *Risk Manager* mendeteksi volatilitas ekstrem atau *Technical Agent* mendeteksi *death cross*, *Portfolio Manager Agent (CIO)* akan menyeimbangkan konsensus secara objektif.
* **Fault Tolerance Tingkat Tinggi**: Jika salah satu API eksternal (misalnya *Finnhub* atau *FRED*) mengalami gangguan jaringan, node yang bersangkutan akan mengaktifkan mekanisme *offline deterministic fallback* tanpa menghentikan atau merusak keseluruhan eksekusi graf multi-agen.

---

## 🛠️ Daftar Alat & Teknologi yang Digunakan (`Tools & Libraries Used`)

### 1. Bahasa Pemrograman & Runtime Backend
* **Python 3.13+**: Runtime berkinerja tinggi dengan dukungan *type hinting* dan *concurrency* modern.
* **FastAPI & Uvicorn**: Framework web asinkron untuk penyediaan REST API endpoint (`/api/v1/analyze`, `/api/v1/backtest`) serta *WebSocket multiplexing* (`/api/v1/ws/live`).
* **Pydantic v2**: Validasi skema data ketat untuk input/output agen, menjamin integritas struktur *JSON* dan keamanan kontrak API.
* **AsyncIO**: Manajemen I/O non-blocking untuk panggilan API paralel dan eksekusi grafik (*graph execution*).

### 2. Kecerdasan Buatan & Multi-Agent Framework
* **Google Gemini 3.1 Flash-Lite (`google-genai`)**: Model penalaran bahasa tingkat lanjut (*State-of-the-Art Reasoning Engine*) yang ditugaskan untuk analisis sentimen berita fundamental, ekstraksi katalis peristiwa, sintesis makroekonomi, dan artikulasi keputusan akhir CIO.
* **LangGraph (`StateGraph`)**: Framework pengatur alur kerja multi-agen yang mengelola transisi status bersyarat (*conditional edges*), penanganan *retry* otomatis, dan pemeliharaan riwayat eksekusi agen.
* **LangChain**: Integrasi utilitas dan pemodelan prompt terstruktur.

### 3. Komputasi Kuantitatif & Pemodelan Machine Learning
* **pandas, numpy, polars, scipy**: Pustaka komputasi matriks dan pemrosesan deret waktu (*time-series*) untuk kalkulasi retur logaritmik, volatilitas bergulir (*rolling volatility*), dan manipulasi *DataFrame* kecepatan tinggi.
* **scikit-learn**: Pembangunan jalur rekayasa fitur (*StandardScaler*), serta pelatihan model prediksi `RandomForestClassifier` dan `GradientBoostingClassifier`.
* **LightGBM & XGBoost**: Model *Gradient Boosted Decision Trees* (*GBDT*) yang dilatih secara dinamis oleh *ML Prediction Agent* untuk memproyeksikan target harga saham dalam cakupan waktu 5 hari ke depan.
* **yfinance**: Pengambilan data harga *spot* real-time, riwayat bar `OHLCV` hingga 5 tahun, jadwal dividen, rantai opsi (*Option Chains - Calls/Puts*), dan laporan keuangan fundamental perusahaan.

### 4. API Data Finansial & Berita Eksternal (`.env` Configurable)
* **Finnhub API**: Aliran berita perusahaan dan indikator sentimen institusional.
* **Alpha Vantage API**: Metrik makroekonomi dan sentimen berita keuangan global.
* **Financial Modeling Prep (FMP) API**: Kalender pendapatan (*Earnings Calendar*) dan profil emiten lengkap.
* **NewsAPI**: Agregasi judul berita dari media finansial internasional (*Bloomberg, Reuters, WSJ*).
* **Federal Reserve Economic Data (FRED) API**: Pemantauan langsung kurva imbal hasil obligasi AS (*Treasury Yield Curve*) dan suku bunga acuan The Fed.

### 5. Basis Data, Caching & Antrean Tugas Terdistribusi
* **Redis (`redis.asyncio`)**: Sistem *caching* in-memory terdistribusi (`df_ohlcv:*`, `market_data_output:*`) serta infrastruktur *Pub/Sub WebSocket* untuk transmisi log eksekusi agen secara *real-time*.
* **MongoDB (`Motor` Async Driver)**: Penyimpanan dokumen asinkron untuk mencatat riwayat run analisis kuantitatif, log *backtesting*, dan rekam jejak rekomendasi perdagangan (dilengkapi mekanisme *fallback in-memory* otomatis jika server database offline).
* **Celery / ARQ (`celery -A celery_app.celery_app worker`)**: Sistem antrean pemrosesan latar belakang (*Background Task Queue*) untuk menjalankan simulasi kuantitatif berat dan pemindaian *watchlist* terjadwal tanpa membebani server utama.

---

## 🤖 10 Agen Kuantitatif Spesialistik (`The Specialized Agents`)

Setiap agen memiliki tanggung jawab kuantitatif yang terisolasi secara modular, menghasilkan output berbasis Pydantic (`models/schemas.py`) yang ditransmisikan ke dalam *state graph global*:

### 1. Market Data Agent (`agents/market_data_agent.py`)
* **Peran**: Menyerap harga pasar terkini, rentang batas statistik mingguan/tahunan, dan data fundamental neraca keuangan.
* **Output Kuantitatif**: Harga *spot* terkini (`USD`), perubahan harga harian absolut & persentase, batas tertinggi/terendah 52 minggu, rasio valuasi fundamental (`P/E`, `P/B`, `EV/EBITDA`), rasio dividen, serta *array* bar `OHLCV` (Open, High, Low, Close, Volume) lengkap.

### 2. Quantitative Historical Regime Agent (`agents/historical_regime_agent.py`)
* **Peran**: Mengevaluasi riwayat harga harian hingga 5 tahun (1.260+ bar trading) untuk mengaudit kinerja jangka panjang emiten.
* **Output Kuantitatif**:
  * **Compound Annual Growth Rate (CAGR)**: `1-Year CAGR`, `3-Year CAGR`, dan `5-Year CAGR` (%).
  * **Rasio Imbal Hasil Terkoreksi Risiko**: `Sharpe Ratio` & `Sortino Ratio` tahunan terhadap siklus 5 tahun.
  * **Statistik Risiko Ekor (*Tail Risk*)**: `Maximum Drawdown (%)` dan `95% Daily Tail Value-at-Risk (VaR)`.
  * **Klasifikasi Rezim Volatilitas & Siklus**: Mengidentifikasi apakah saham berada dalam *Breakout Expansion Regime*, *Low Volatility Compression*, atau *Secular Compounder*.
  * **Monthly Seasonality Heatmap**: Kalkulasi rata-rata persentase retur dan probabilitas kemenangan (*Win Probability*) untuk setiap bulan kalender (`Januari` hingga `Desember`).

### 3. Deterministic Technical Analysis Agent (`agents/technical_analysis_agent.py`)
* **Peran**: Melakukan komputasi matematis deterministik 100% atas 11 indikator teknikal utama tanpa estimasi LLM.
* **Output Kuantitatif**:
  * **MACD Line**: Nilai pasti `macd_line`, `signal_line`, dan `histogram` (`Bullish Cross` / `Bearish Cross`).
  * **Ichimoku Cloud**: Nilai pasti `tenkan_sen` (Conversion Line), `kijun_sen` (Base Line), `senkou_span_a/b`, dan status awan (`Above Cloud - Bullish` / `Below Cloud - Bearish`).
  * **Oscillators & Moving Averages**: `RSI (14)`, `SMA 20/50/200` (`Golden Cross` / `Death Cross`), `EMA 9/21`, `Bollinger Bands` (batas atas/tengah/bawah & rasio lebar band), `ATR (14) Volatility`, `VWAP`, `ADX (14) Trend Strength`, `OBV (On-Balance Volume)`, dan `Stochastic RSI`.
  * **Pengenalan Pola Grafik**: Deteksi algoritmis atas pola klasik (`Double Bottom`, `Bull Flag`, `Ascending Triangle`).

### 4. News Intelligence Agent (`agents/news_intelligence_agent.py`)
* **Peran**: Melakukan agregasi berita institusional terbaru dari multi-sumber eksternal (`Finnhub`, `Alpha Vantage`, `FMP`, `NewsAPI`, `yfinance`) dan memanfaatkan **Google Gemini 3.1 Flash-Lite** untuk penalaran sentimen mendalam.
* **Output Kuantitatif**: Klasifikasi sentimen AI (`Bullish`, `Bearish`, `Neutral`), skor sentimen numerik (`-100 hingga +100`), persentase keyakinan model (%), ringkasan eksekutif berita, ekstraksi peristiwa katalis (`Earnings Beats`, `Analyst Upgrades/Downgrades`, `Product Launches`, `SEC Filings`), dan daftar tautan artikel asli.

### 5. Macro Economy Agent (`agents/macro_economy_agent.py`)
* **Peran**: Mengevaluasi iklim makroekonomi berdasarkan kebijakan bank sentral dan indikator makro.
* **Output Kuantitatif**: Suku Bunga The Fed (`Fed Funds Rate %`), Kurva Imbal Hasil (`10Y-2Y Treasury Spread` & status inversi), Tingkat Inflasi CPI, Pertumbuhan PDB Real, Tingkat Pengangguran, serta Skor Rezim Makro (`Goldilocks Expansion`, `Stagflationary Pressure`, `Monetary Tightening`).

### 6. Options Flow Agent (`agents/options_flow_agent.py`)
* **Peran**: Menganalisis struktur rantai opsi (*Options Chains*) untuk mendeteksi posisi *hedging* bandar/dealer (*Gamma Exposure*).
* **Output Kuantitatif**: `Put/Call Volume Ratio`, Total Open Interest, `Max Pain Strike Price`, Implied Volatility (IV) Skew, `Call Wall Strike` (level resistensi gamma terbesar), dan `Put Wall Strike` (level support/gamma pin terbesar).

### 7. Risk Manager Agent (`agents/risk_manager_agent.py`)
* **Peran**: Melakukan manajemen risiko institusional dan alokasi anggaran risiko portofolio.
* **Output Kuantitatif**: Rekomendasi batas maksimal alokasi modal (`%` berbasis `Kelly Criterion` & penyesuaian volatilitas), rekomendasi harga *Stop-Loss* (`$` dan `%` di bawah entry), harga target *Take-Profit* (`$`), rasio *Risk-to-Reward* (`1 : 2.5+`), serta evaluasi korelasi *Beta* terhadap indeks pasar acuan.

### 8. Machine Learning Prediction Agent (`agents/ml_prediction_agent.py`)
* **Peran**: Melatih konsensus model *Machine Learning Ensemble* secara dinamis menggunakan fitur deret waktu yang direkayasa (*momentum, standar deviasi bergulir, lonjakan volume*).
* **Output Kuantitatif**: Proyeksi harga target 5 hari ke depan (`USD`), ekspektasi persentase pergerakan (`%`), tingkat keyakinan model (`0-100%`), serta rincian prediksi individual dari model `LightGBM`, `XGBoost`, dan `RandomForest`.

### 9. Chief Investment Officer (CIO) Portfolio Manager Agent (`agents/portfolio_manager_agent.py`)
* **Peran**: Bertindak sebagai manajer investasi eksekutif yang membobot seluruh 8 agen kuantitatif sebelumnya untuk merumuskan keputusan akhir.
* **Output Kuantitatif**:
  * **Skor Konfluensi Master**: Nilai kuantitatif gabungan dari rentang `0 hingga 100`.
  * **Mandat Investasi Institusional**: **`STRONG BUY`**, **`BUY`**, **`HOLD`**, **`SELL`**, atau **`STRONG SELL`**.
  * **Cakupan Waktu Investasi (Investment Horizon)**: Ditentukan secara dinamis berdasarkan mesin kuantitatif luring (*offline fallback engine*) menggunakan selisih ekstrimitas dari Skor Konfluensi atau secara analitis oleh Agen AI Gemini. Horizon yang direkomendasikan adalah `1 Week`, `1 Month`, atau `6 Months` hingga `1 Year`.
  * **Target Harga Cakupan 12 Bulan (`USD`)**.
  * **Tesis Bullish vs Bearish**: Penjelasan rasional kuantitatif dan fundamental yang mendasari rekomendasi.

### 10. Execution Agent (`agents/execution_agent.py`)
* **Peran**: Menyusun protokol eksekusi perdagangan agar eksekusi order tidak mengganggu likuiditas pasar (*Slippage Management*).
* **Output Kuantitatif**: Rekomendasi tipe order (`Limit Order` vs `Market Order`), strategi pemecahan order algoritmis (`VWAP / TWAP Iceberg Splitting`), zona masuk optimal (*Entry Zone $*), pemicu *Stop-Loss/Take-Profit*, dan catatan kepatuhan simulasi.

---

## 🚀 Cara Menjalankan Proyek (Backend Kuantitatif)

Sistem ini dapat dijalankan sepenuhnya melalui perintah terminal di dalam direktori `backend/`.

### 1. Prasyarat Sistem
* **Python 3.13+**
* **Redis Server** (berjalan pada port `6379`)
* **MongoDB** (opsional, sistem memiliki *fallback repository in-memory* otomatis jika MongoDB tidak diaktifkan)

### 2. Instalasi Dependensi & Lingkungan Virtual (`.venv`)
```bash
cd backend

# Buat virtual environment Python
python3 -m venv .venv
source .venv/bin/activate

# Install seluruh pustaka kuantitatif, ML, dan API
pip install -r requirements.txt
```

### 3. Konfigurasi Variabel Lingkungan (`.env`)
Salin file konfigurasi contoh dan masukkan API key Anda (seperti `GEMINI_API_KEY`, `FINNHUB_API_KEY`, `ALPHA_VANTAGE_API_KEY`):
```bash
cp .env.example .env
```

### 4. Menjalankan Server API Asinkron (`FastAPI & Uvicorn`)
Jalankan server *Uvicorn* untuk mengaktifkan REST API endpoint dan WebSocket port `8000`:
```bash
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
* **Dokumentasi Interaktif API (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Endpoint Analisis Utama**: `POST http://localhost:8000/api/v1/analyze` dengan payload JSON `{"ticker": "AAPL"}`.

### 5. Menjalankan Celery Background Worker (Opsional untuk Tugas Berat)
Buka terminal baru di dalam folder `backend/` untuk menjalankan *worker* tugas latar belakang:
```bash
source .venv/bin/activate
celery -A celery_app.celery_app worker --loglevel=info --concurrency=4
```

### 6. Alternatif: Menjalankan dengan Docker Compose
Jika Anda ingin menjalankan seluruh kontainer *backend*, *Redis*, *MongoDB*, dan *Celery Worker* sekaligus:
```bash
docker compose up --build -d
```

---

## 🔒 Catatan Kepatuhan Simulasi Institusional
Mesin Kuantitatif `SHF` ini dirancang murni untuk keperluan riset ilmiah, evaluasi algoritme, dan pendidikan finansial kuantitatif. Seluruh data, prediksi model *Machine Learning*, dan rekomendasi perdagangan yang dihasilkan oleh 10 agen AI berada dalam mode evaluasi simulasi (`SIMULATION ONLY - NO REAL MONEY ORDERS PLACED`). Selalu lakukan manajemen risiko mandiri sebelum menempatkan modal riil di pasar modal.
