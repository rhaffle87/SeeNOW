# Chapter 12: Features and Management of FusionAccess

## 1. Manajemen Kebijakan Akses (Policy Management)
FusionAccess menyediakan kontrol keamanan granular yang dapat diterapkan pada level sistem, Desktop Group, atau akun pengguna tertentu:

### A. Periferal & Redirection Policy
- **USB Redirection Policy:**
  - *Blacklist / Whitelist:* Membatasi jenis perangkat USB berdasarkan Class ID, Vendor ID (VID), atau Product ID (PID).
  - Mengizinkan keyboard dan mouse, namun memblokir USB mass storage (flashdisk/HDD eksternal) untuk mencegah kebocoran data rahasia perusahaan.
- **Clipboard Redirection:**
  - Mengontrol aksi copy-paste teks dan file:
    - *Bidirectional:* Dua arah (Client <-> Virtual Desktop).
    - *Client to Agent Only:* Hanya bisa paste dari lokal ke VM (mencegah eksfiltrasi data ke laptop pribadi).
    - *Disabled:* Fitur copy-paste dimatikan total.
- **File / Drive Redirection:**
  - Memetakan hard disk lokal pengguna ke dalam file explorer Windows virtual desktop.

### B. Display & Watermark Security
- **Dynamic Screen Watermark:**
  - Menampilkan watermark transparan di layar sesi pengguna (berisi nama akun user, IP address, dan timestamp real-time).
  - Efektif mencegah kebocoran data melalui foto kamera smartphone terhadap layar monitor.
- **Adaptive Display Quality:**
  - Mengatur rasio kompresi gambar dan frame rate secara dinamis berdasarkan kondisi bandwidth jaringan klien.

---

## 2. Pemeliharaan Rutin & Operasional (Routine O&M)
- **Session Management:**
  - Administrator dapat memantau sesi pengguna yang sedang aktif, memutus paksa sesi bermasalah (*Disconnect*), melakukan logout paksa (*Log Off*), atau mengirim pesan notifikasi siaran (*Broadcast Message*).
- **Alarm & Health Monitoring:**
  - Memonitor metrik utilisasi CPU, memori, bandwidth jaringan, dan status heartbeat setiap komponen (HDC, ITA, WI, vAG, vLB).
  - Notifikasi alarm otomatis via email atau SMS saat terjadi gangguan kritis.
- **Backup & Disaster Recovery:**
  - Melakukan backup harian otomatis terhadap database GaussDB FusionAccess dan konfigurasi ITA.
  - Memastikan sistem dapat di-restore dengan cepat jika terjadi kegagalan hardware fisik data center.
