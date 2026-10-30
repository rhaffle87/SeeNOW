# Chapter 10: Planning and Deployment of FusionAccess

## 1. Skema Deployment FusionAccess

| Mode Deployment | Deskripsi | Jumlah Pengguna | Lingkungan Rekomendasi |
|---|---|---|---|
| **All-in-One Deployment** | Seluruh komponen (ITA, HDC, WI, vAG, vLB, GaussDB) diinstal dalam 1 atau 2 VM bersamaan. | $\le 50$ Pengguna | Lab pengujian, POC (Proof of Concept), kantor cabang sangat kecil. |
| **Standard / Separated Deployment** | Setiap komponen (ITA, HDC, WI, vAG/vLB) diinstal pada VM independen terpisah. | $50 - 1000+$ Pengguna | Lingkungan produksi enterprise skala menengah hingga besar. |
| **HA (High Availability) Cluster** | Setiap komponen dideploy dalam pasangan Active/Standby atau Load Balancing (2x ITA, 2x HDC, 2x WI, 2x vAG, 2x vLB). | Enterprise Skala Penuh | Menghilangkan *single point of failure* pada seluruh layer akses dan kontrol. |

---

## 2. Rencana Jaringan & Port Kunci FusionAccess
Untuk menjamin komunikasi antar-komponen aman dan lancar, firewall internal harus membuka port komunikasi standar:
- **Port 8448:** Akses Web GUI Admin ITA (HTTPS).
- **Port 443:** Akses Web GUI User WI dan gerbang vAG (HTTPS).
- **Port 80:** Akses HTTP redirect ke HTTPS pada vLB / WI.
- **Port 8443:** Akses API FusionCompute VRM.
- **Port 53:** Layanan DNS Server (UDP/TCP).
- **Port 88 / 389 / 636:** Layanan Microsoft Active Directory Kerberos / LDAP / LDAPS.
- **Port 28511 - 28521:** Port transmisi protokol desktop Huawei HDP antara Client, vAG, dan HDP Agent.

---

## 3. Tahapan Instalasi & Inisialisasi FusionAccess
1. **Penyediaan Infrastruktur Dasar:**
   - Install dan konfigurasi Active Directory (AD), DNS Server, dan DHCP Server.
   - Buat Organizational Unit (OU) khusus di AD untuk pengguna desktop dan akun komputer virtual desktop.
2. **Deploy VM Komponen Manajemen:**
   - Deploy VM Linux/Windows untuk ITA, HDC, WI, GaussDB, vAG, dan vLB menggunakan ISO installer FusionAccess.
3. **Inisialisasi Sistem via Wizard ITA:**
   - Akses portal ITA: `https://<ITA_IP>:8448`.
   - **Koneksi ke Virtualization Platform:** Daftarkan IP VRM FusionCompute beserta kredensial akun admin agar ITA dapat memerintahkan pembuatan VM desktop.
   - **Konfigurasi Domain Controller:** Masukkan FQDN domain AD (misal: `corp.domain.com`), username dan password Domain Admin.
   - **Konfigurasi HDC & WI:** Masukkan IP instance HDC dan WI yang terdaftar.
   - **Koneksi Database:** Masukkan kredensial database GaussDB untuk retensi data sistem.
