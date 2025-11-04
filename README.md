<div align='center'>
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Poppins&weight=600&size=38&pause=1000&color=0B84F3&center=true&vCenter=true&width=800&height=70&lines=Project+NetFast;Website+Pemesanan+WiFi+dan+Teknisi;Project+Basis+Data" alt="Typing SVG" />
  </a>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/Basis%20Data-MySQL-blue?style=for-the-badge&logo=mysql" alt="MySQL Badge">
  <img src="https://img.shields.io/badge/Backend-Django-green?style=for-the-badge&logo=django" alt="Django Badge">
  <img src="https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python" alt="Python Badge">
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange?style=for-the-badge&logo=html5" alt="Frontend Badge">
  <img src="https://img.shields.io/badge/Platform-Web-informational?style=for-the-badge&logo=google-chrome" alt="Web Platform Badge">
</p>

---

## 🌐 Tentang Proyek

**NetFast** adalah website layanan WiFi berbasis *Django* dan *MySQL* yang membantu pelanggan untuk:
- Melihat dan memesan paket WiFi  
- Mengukur kecepatan internet secara real-time  
- Memanggil teknisi untuk instalasi atau perbaikan jaringan  

Proyek ini merupakan tugas dari mata kuliah **Basis Data**, dengan fokus pada penerapan sistem informasi berbasis web dan manajemen data relasional.

---

## ⚙ Fitur Utama

✅ Login & registrasi (Admin, Pelanggan, Teknisi)  
📦 Pemesanan paket WiFi online  
🚀 Pengukuran kecepatan internet (Speed Test)  
🧰 Pemanggilan teknisi untuk instalasi/perbaikan  
📊 Dashboard admin & laporan pelanggan  
💾 Database MySQL dengan autentikasi berbasis role  

---

## 🧩 Teknologi yang Digunakan

| Komponen | Teknologi |
|-----------|------------|
| *Frontend* | HTML, CSS, JavaScript, Bootstrap |
| *Backend* | Python (Django Framework) |
| *Database* | MySQL |
| *Version Control* | Git & GitHub |

---

## 🧑‍💻 Tim Kontributor

| NAMA | NIM |
| ------- | -------- |
| **[Izaz Tsany Rismawan](https://github.com/IzazTsany14)** | 24111814088 |
| **[Hanna Maulidhea](https://github.com/maulidhea)** | 24111814091 |
| **[Keisa Aushafa Dzihni](https://github.com/KeisaAushafa)** | 24111814109 |

---

## 🚀 Status Proyek

🟢 *Sedang dalam tahap pengembangan (Development Stage)*  
🔜 Fitur berikutnya: Integrasi *API Speedtest* & *Notifikasi Real-Time*

---

## Setup Project

Pertama pastikan anda ada pada folder project ini yang telah berhasil anda klon
jika belum silahkan clone dengan command
```bash
git clone --depth=1 https://github.com/IzazTsany14/project-basis-data

# masuk kedalam folder clone
cd project-basis-data

# buat virtual environment python
python -m venv .venv

# aktifkan venv python
## powershell
## windows
.venv/Scrips/activate.ps1
## bash
## non windows
source .venv/bin/activate.sh

# install package yang diperlukan
pip install -r requirements.txt

# jalanin server
cd NetFastProject
python NetFastProject/manage.py runserver
```
