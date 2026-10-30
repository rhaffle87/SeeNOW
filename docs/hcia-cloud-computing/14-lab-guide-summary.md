# Chapter 14: HCIA-Cloud Computing V5.5 Lab Guide Summary

Ringkasan praktikum esensial dari 526 halaman panduan lab resmi Huawei HCIA-Cloud Computing V5.5.

---

## Lab 1: Konfigurasi Awal FusionCompute VRM
- **Akses Portal:**
  - Login web browser: `https://<VRM_IP>:8443` (Default User: `admin`).
  - Verifikasi status CNA host yang terdaftar dalam cluster (Status: Normal, CPU/RAM usage metric hijau).
- **Konfigurasi Fundamental:**
  - Konfigurasi NTP Time Server (Wajib sinkron detik antar VRM dan seluruh host CNA).
  - Pembuatan Data Center logis (Site) dan penambahan Cluster komputasi.
  - Penambahan Host CNA ke dalam Cluster via VRM Web GUI.

---

## Lab 2: Konfigurasi Storage Virtualization
- **Langkah Kerja:**
  1. **Konfigurasi IP SAN / iSCSI Target:**
     - Masuk ke menu Storage -> Storage Resource -> Add Storage Resource.
     - Pilih tipe: `IP-SAN`. Masukkan IP Service Storage Server dan Initiator Name host CNA.
  2. **Scan Storage Device:**
     - Lakukan scan LUN dari storage controller untuk mengenali disk volume fisik.
  3. **Inisialisasi Data Storage:**
     - Tambahkan Data Storage baru bertipe `Virtualized` (sistem file VIMS).
     - Format dan kaitkan Data Storage tersebut ke semua host CNA dalam cluster agar menjadi shared storage.

---

## Lab 3: Konfigurasi Network Virtualization (DVS & Port Group)
- **Langkah Kerja:**
  1. **Membuat Distributed Virtual Switch (DVS):**
     - Menu Network -> Distributed Virtual Switch -> Create DVS.
     - Berikan nama DVS (misal: `DVS-Management-Business`).
  2. **Menambahkan Uplink:**
     - Pilih antarmuka jaringan fisik (NIC) dari masing-masing host CNA yang terhubung ke switch fisik.
     - Konfigurasi mode agregasi/bonding: `Active/Standby` atau `Load Balancing based on IP Hash (LACP)`.
  3. **Membuat Port Group:**
     - Tambahkan Port Group untuk traffic VM Bisnis (misal: `PG_VM_VLAN10`).
     - Tentukan VLAN ID (misal: VLAN 10 untuk segmentasi traffic VM).

---

## Lab 4: Manajemen Siklus Hidup VM & Live Migration
- **Pembuatan VM:**
  - Tetapkan vCPU, Memory, Virtual Disk (Thin Provisioning pada VIMS Data Storage), dan kaitkan ke Port Group `PG_VM_VLAN10`.
  - Mount file ISO sistem operasi (Windows / EulerOS).
- **Instalasi Huawei UVP VM Tools:**
  - Setelah OS terpasang, instal `vmtools` di dalam VM.
  - UVP VM Tools menyediakan driver paravirtualisasi (PV driver) untuk disk dan network, serta sinkronisasi status ke VRM.
- **Pengujian Live Migration:**
  - Klik kanan VM yang sedang berjalan di CNA01 -> pilih **Migrate**.
  - Pilih destination host CNA02.
  - Amati proses live migration: ping terus berjalan ke IP VM dengan packet loss 0% atau paling banyak 1 request timeout sesaat.

---

## Lab 5: Pengujian High Availability (HA) & DRS
- **Konfigurasi Cluster HA:**
  - Aktifkan fitur HA pada level cluster di VRM.
  - Simulasikan insiden host failure: matikan paksa interface atau kabel daya host CNA01.
  - VRM mendeteksi hilangnya detak jantung (heartbeat) CNA01 dalam 30-60 detik.
  - Seluruh VM penting yang sebelumnya berada di CNA01 otomatis di-boot ulang pada host CNA02.
- **Konfigurasi DRS (Dynamic Resource Scheduler):**
  - Tentukan ambang batas utilisasi (misal CPU > 80% atau RAM > 85%).
  - Jalankan simulasi beban CPU tinggi pada VM; amati DRS memicu rekomendasi migrasi otomatis untuk mendistribusikan beban.

---

## Lab 6 & 7: Persiapan Template FusionAccess VDI
- **Persiapan Master Virtual Machine:**
  1. Buat satu VM baru dengan spesifikasi standar (misal: 2 vCPU, 4GB RAM, 50GB Disk).
  2. Instal Windows 10/11 Enterprise.
  3. Instal software aplikasi bisnis standar (Office, Browser, PDF Reader).
  4. Instal **Huawei Desktop Protocol (HDP) Agent**.
  5. Jalankan utilitas Windows `Sysprep` untuk mereset Security Identifier (SID) dan informasi unik mesin.
  6. Matikan VM dan konversikan VM menjadi **Template Induk (Golden Image)** di VRM.

---

## Lab 8: Provisioning Virtual Desktop Terdistribusi
- **Langkah Kerja di Portal ITA Admin FusionAccess:**
  1. Login ke portal ITA: `https://<ITA_IP>:8448`.
  2. Hubungkan ITA ke Domain Controller (Microsoft Active Directory) untuk sinkronisasi grup user.
  3. Buat Desktop Group baru:
     - Pilih tipe provisioning: **Linked Clone**.
     - Tentukan Template Induk yang dibuat pada Lab 7.
     - Pilih Data Storage tujuan dan Port Group jaringan desktop.
     - Tentukan jumlah VM yang akan dibuat (misal: 10 desktop).
  4. Tetapkan kebijakan akses (Policy):
     - USB Redirection: Enabled untuk flashdisk, Disabled untuk storage eksternal tak dikenal.
     - Clipboard Redirection: Bidirectional atau Client to Agent only.
  5. Alokasikan Desktop Group ke grup pengguna AD (misal: `Domain Users / Finance Team`).
- **Verifikasi Sisi Pengguna Akhir:**
  1. Buka browser di perangkat client dan akses URL portal WI: `https://<vLB_IP>/wi`.
  2. Masukkan username dan password domain Windows.
  3. Klik ikon Virtual Desktop yang muncul; aplikasi HDP Client meluncurkan desktop virtual secara instan.
