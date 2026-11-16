# Bike Sharing Analysis — Dicoding Final Project

## Isi folder
- `Bike_Sharing_Analysis.ipynb`: notebook analisis lengkap dari business questions, data gathering, assessing, cleaning, EDA, visualisasi, binning/manual grouping, hingga kesimpulan dan action items.
- `app.py`: dashboard interaktif Streamlit.
- `day.csv`, `hour.csv`: data sumber yang disediakan.
- `Readme.txt`: dokumentasi dataset asli.
- `requirements.txt`: dependensi Python.

## Menjalankan notebook
1. Buka folder ini di VS Code/Jupyter atau unggah notebook dan CSV ke Google Colab.
2. Pastikan `day.csv` dan `hour.csv` berada satu folder dengan notebook.
3. Jalankan semua cell dari atas ke bawah.

## Menjalankan dashboard secara lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```
Dashboard akan terbuka di browser lokal.

## Deploy ke Streamlit Community Cloud
1. Buat repository GitHub baru dan unggah seluruh isi folder ini.
2. Buka https://share.streamlit.io/ dan login menggunakan GitHub.
3. Pilih repository, branch, dan file utama `app.py`.
4. Deploy. Pastikan `day.csv`, `hour.csv`, dan `requirements.txt` ikut berada di root repository.
5. Uji URL publik setelah deploy dan cantumkan tautan tersebut pada submission.

**Catatan penting:** deploy cloud membutuhkan akun dan tindakan autentikasi pemilik akun. File proyek ini sudah disiapkan agar dapat dideploy, tetapi deployment publik belum dilakukan dari sini.

## Catatan metodologi
- Rentang data: 1 Januari 2011 sampai 31 Desember 2012.
- `day.csv` digunakan untuk tren harian/musiman dan cuaca; `hour.csv` digunakan untuk pola per jam.
- `temp`, `atemp`, `hum`, dan `windspeed` merupakan variabel ternormalisasi.
- Analisis bersifat deskriptif/asosiatif; jangan menyimpulkan kausalitas.
- Dataset dan paper asal: Fanaee-T, H. & Gama, J. (2013), https://doi.org/10.1007/s13748-013-0040-3
