# Chapter 03: Storage Technology Basics

## 1. Arsitektur Storage Tradisional

```
+-----------------------------------------------------------------------------+
| DAS (Direct-Attached) | NAS (Network-Attached)    | SAN (Storage Area Net)  |
+-----------------------+---------------------------+-------------------------+
| Disk terpasang kabel  | Akses file via LAN        | Jaringan blok khusus    |
| langsung ke host bus  | Protokol: NFS / CIFS      | Protokol: FC / iSCSI    |
| Tidak bisa di-share   | Berbasis File Level       | Berbasis Block Level    |
| Cocok: PC / Server 1  | Cocok: File Sharing & NAS | Cocok: DB & Hypervisor  |
+-----------------------+---------------------------+-------------------------+
```

### A. DAS (Direct-Attached Storage)
- Storage terhubung langsung ke satu host fisik melalui kabel internal SAS atau eksternal SCSI/SATA.
- Kelemahan: Kapasitas tidak dapat dibagi secara dinamis ke host lain; memicu pemborosan kapasitas (storage island).

### B. NAS (Network-Attached Storage)
- Perangkat penyimpanan berbasis file yang terhubung ke jaringan LAN standar IP/Ethernet.
- Akses data menggunakan protokol file-sharing:
  - **NFS (Network File System):** Standar sistem operasi Linux / Unix.
  - **CIFS / SMB (Common Internet File System):** Standar sistem operasi Windows.
- Cocok untuk penyimpanan dokumen, repository gambar, dan backup data tidak berlatensi kritis.

### C. SAN (Storage Area Network)
- Jaringan khusus berkecepatan tinggi yang menghubungkan kumpulan server ke pool disk array terpusat.
- Akses data berbasis level blok (Block-Level I/O) di mana host melihat volume storage sebagai disk lokal fisik (LUN - Logical Unit Number).
- **Dua Tipe Utama SAN:**
  1. **FC SAN (Fibre Channel SAN):** Menggunakan kabel serat optik dan switch FC khusus. Throughput 8G/16G/32Gbps, latensi ultra-rendah, biaya perangkat relatif tinggi.
  2. **IP SAN (iSCSI):** Membungkus perintah SCSI dalam paket TCP/IP melalui jaringan Ethernet standar. Biaya murah, fleksibel, mudah dikonfigurasi via kartu jaringan standar (NIC).

---

## 2. Klasifikasi Tipe Layanan Storage Modern
1. **Block Storage (Penyimpanan Blok):**
   - Mengakses data sebagai blok raw byte (seperti hard drive kosong).
   - Performa read/write sangat cepat, cocok untuk database relational (Oracle, MySQL, GaussDB) dan virtual disk VM hypervisor.
2. **File Storage (Penyimpanan Berkas):**
   - Mengakses data dengan struktur hierarki folder dan direktori file.
   - Mendukung multi-user read/write bersamaan, cocok untuk shared folder kantor dan web asset.
3. **Object Storage (Penyimpanan Objek):**
   - Menyimpan data tanpa struktur pohon hierarki; setiap data diperlakukan sebagai objek dengan metadata unik dan Global Unique ID (UUID).
   - Diakses melalui HTTP/HTTPS REST API (GET, PUT, DELETE).
   - Skalabilitas tak terbatas (petabytes ke exabytes), durabilitas sangat tinggi, biaya per GB sangat murah. Contoh: Huawei Cloud OBS, AWS S3.
