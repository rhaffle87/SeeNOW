# Chapter 01: Cloud Computing Basics

## 1. IT Basics
- **Evolusi Arsitektur Komputasi:**
  - **Era Mainframe (1960-an):** Komputasi terpusat terspesialisasi tinggi, biaya sangat mahal, skalabilitas vertikal terbatas, arsitektur proprietary.
  - **Era Client/Server & PC (1980-an):** Muncul server berbasis x86 standar industri, komputasi terdistribusi, biaya perangkat keras menurun drastis.
  - **Era Internet & Data Center Modern (2000-an):** Ledakan data dan aplikasi web multi-tier (Web Server, App Server, DB Server).
- **Tantangan Arsitektur IT Tradisional Silo (Silo Architecture):**
  - Utilisasi resource rendah (rata-rata server x86 tradisional hanya terpakai 10% - 15%).
  - Biaya investasi (CAPEX) dan operasional (OPEX) tinggi (listrik, pendingin/cooling, space data center).
  - Siklus provisioning layanan sangat lambat (memerlukan berminggu-minggu untuk pengadaan dan instalasi hardware baru).
  - Ketergantungan tinggi pada hardware fisik tertentu (*vendor lock-in* dan *single point of failure*).

---

## 2. About Cloud Computing
- **Definisi Standar NIST (National Institute of Standards and Technology):**
  - Cloud computing adalah model yang memungkinkan akses jaringan on-demand yang nyaman ke kumpulan bersama (shared pool) dari sumber daya komputasi yang dapat dikonfigurasi (misal: jaringan, server, penyimpanan, aplikasi, dan layanan), yang dapat disediakan dan dirilis dengan cepat melalui upaya manajemen minimal atau interaksi penyedia layanan minimal.
- **5 Karakteristik Esensial Cloud Computing (NIST):**
  1. **On-Demand Self-Service:** Konsumen dapat memesan resource komputasi secara mandiri tanpa interaksi manual dengan admin penyedia.
  2. **Broad Network Access:** Resource dapat diakses melalui jaringan standar menggunakan berbagai perangkat (laptop, smartphone, thin client).
  3. **Resource Pooling:** Sumber daya komputasi penyedia dikumpulkan untuk melayani banyak konsumen menggunakan model multi-tenant, dengan alokasi dinamis fisik dan virtual.
  4. **Rapid Elasticity:** Kemampuan scaling up/down secara cepat dan fleksibel sesuai kebutuhan beban kerja.
  5. **Measured Service:** Penggunaan resource dikontrol, dimonitor, dan ditagihkan berdasarkan konsumsi aktual (*pay-as-you-go*).
- **3 Model Layanan (Service Models):**
  - **IaaS (Infrastructure as a Service):**
    - Menyediakan resource komputasi dasar: CPU virtual, memori, storage, dan network.
    - Pengguna mengelola: OS, middleware, runtime aplikasi, data.
    - Vendor mengelola: Perangkat keras fisik, fasilitas DC, dan layer virtualisasi hypervisor.
    - Contoh: Huawei ECS, AWS EC2, OpenStack Nova.
  - **PaaS (Platform as a Service):**
    - Menyediakan lingkungan pengembangan dan eksekusi aplikasi (runtime, database engine, container cluster).
    - Pengguna mengelola: Kode aplikasi dan data bisnis.
    - Vendor mengelola: OS, patch keamanan, runtime environment, infrastruktur server dan storage.
    - Contoh: Huawei Cloud RDS/CCE, Google App Engine.
  - **SaaS (Software as a Service):**
    - Menyediakan aplikasi lengkap siap pakai yang diakses via web browser atau client API.
    - Pengguna mengelola: Konfigurasi data pengguna dan akses akun.
    - Vendor mengelola: Seluruh lapisan dari infrastruktur, OS, hingga software aplikasi.
    - Contoh: Office 365, Huawei WeLink, Salesforce.
- **4 Model Deployment (Deployment Models):**
  - **Public Cloud:** Infrastruktur dimiliki dan dioperasikan oleh penyedia pihak ketiga untuk publik umum via internet terbuka.
  - **Private Cloud:** Infrastruktur didedikasikan secara eksklusif untuk satu organisasi tunggal, memberikan kontrol dan keamanan data tertinggi.
  - **Hybrid Cloud:** Kombinasi dua atau lebih model (public dan private cloud) yang terikat bersama oleh teknologi standar yang memungkinkan portabilitas data dan aplikasi.
  - **Community Cloud:** Infrastruktur dibagi oleh beberapa organisasi dengan kepentingan atau persyaratan kepatuhan/keamanan yang sama.

---

## 3. Mainstream Cloud Vendors & Technologies
- **Vendor Utama:**
  - **Huawei Cloud / Huawei Digital Power:** Solusi FusionSphere, FusionCompute, FusionAccess, GaussDB, ModelArts.
  - **AWS, Microsoft Azure, Google Cloud:** Layanan hyper-scale global.
- **Teknologi Fondasi:**
  - **Hypervisor KVM (Kernel-based Virtual Machine):** Basis open-source virtualization yang menjadi pondasi modern compute cloud dan Huawei FusionCompute.
  - **OpenStack:** Platform open-source orchestration cloud computing untuk mengelola pool komputasi, storage, dan networking di data center skala besar.
