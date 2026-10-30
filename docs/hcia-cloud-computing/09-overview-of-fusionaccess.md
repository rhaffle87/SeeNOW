# Chapters 09, 10, 11, 12: Huawei FusionAccess Desktop Solution (VDI)

## 1. Overview of FusionAccess
Huawei FusionAccess adalah solusi Virtual Desktop Infrastructure (VDI) enterprise yang menjalankan sistem operasi desktop (Windows/Linux) terpusat di server data center dalam bentuk Virtual Machine, dan menampilkan tampilannya ke pengguna akhir melalui jaringan secara aman dan efisien.

```
+-------------------------------------------------------------------------+
|                              End User Devices                           |
|      (Thin Client TC, PC / Laptop, Tablet / Smartphone, HDP Client)     |
+------------------------------------+------------------------------------+
                                     | (TLS / SSL & HDP Protocol)
                                     v
+-------------------------------------------------------------------------+
|                           Access & Load Balancing                       |
|   +--------------------------+       +------------------------------+   |
|   |   vLB (Virtual Load      |       |   vAG (Virtual Access        |   |
|   |        Balancer)         |       |        Gateway)              |   |
|   +------------+-------------+       +--------------+---------------+   |
+----------------|------------------------------------|-------------------+
                 |                                    |
                 v                                    v
+-------------------------------------------------------------------------+
|                             Management Layer                            |
|   +--------------------------+       +------------------------------+   |
|   |   WI (Web Interface)     |       |   HDC (Huawei Desktop        |   |
|   |   Portal Login User      |       |        Controller)           |   |
|   +--------------------------+       +--------------+---------------+   |
|   +--------------------------+                      |                   |
|   |   ITA (IT Automation)    |                      |                   |
|   |   Portal Admin           |                      |                   |
|   +--------------------------+                      |                   |
|   +--------------------------+       +--------------v---------------+   |
|   |   GaussDB / MS SQL       |       |   AD / DNS / DHCP Server     |   |
|   |   Penyimpanan Konfigurasi|       |   Domain Autentikasi User    |   |
|   +--------------------------+       +------------------------------+   |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  Virtual Desktop Infrastructure Pool                    |
|           (VM Windows 10/11 / Linux dengan HDP Agent Terpasang)         |
|                       Berjalan di FusionCompute                         |
+-------------------------------------------------------------------------+
```

---

## 2. Komponen Inti FusionAccess & Fungsinya

| Komponen | Nama Lengkap | Fungsi Utama |
|---|---|---|
| **ITA** | IT Automation | Menyediakan antarmuka web manajemen bagi administrator sistem untuk membuat VM template, mendefinisikan grup desktop, mengalokasikan desktop ke user/grup, dan mengonfigurasi kebijakan. |
| **HDC** | Huawei Desktop Controller | **Otak inti pengendali sesi.** Mengelola status siklus hidup virtual desktop, menghubungkan user yang login dengan VM yang ditugaskan, memvalidasi hak akses, dan menjaga heartbeat dengan HDP Agent di dalam VM. |
| **WI** | Web Interface | Portal web login untuk pengguna akhir. Setelah login berhasil, WI menampilkan daftar virtual desktop dan aplikasi virtual yang berhak diakses oleh pengguna tersebut. |
| **vAG** | Virtual Access Gateway | Gateway keamanan akses desktop. Berfungsi sebagai proxy protokol HDP dari jaringan eksternal/internet ke jaringan internal virtual desktop, sehingga IP asli VM tidak terekspos langsung. |
| **vLB** | Virtual Load Balancer | Menyeimbangkan beban trafik HTTP/HTTPS antar beberapa node WI dan trafik sesi protokol desktop ke beberapa node vAG menggunakan algoritma load balancing (Round Robin / Least Connection). |
| **DB** | Database (GaussDB) | Menyimpan seluruh metadata sistem, relasi alokasi akun user ke desktop, template data, log audit, dan konfigurasi kebijakan sistem. |
| **AD / DNS** | Active Directory & DNS | Menyediakan layanan otentikasi identitas terpusat (domain Windows AD) untuk akun pengguna dan akun komputer VM desktop, serta resolusi nama domain FQDN. |
| **HDP Agent** | Huawei Desktop Protocol Agent | Software service yang diinstal di dalam setiap VM virtual desktop untuk berkomunikasi dengan HDC dan me-render grafis/audio/USB ke client. |
| **HDP Client** | Client Access Software | Software client yang diinstal di perangkat pengguna (PC, Thin Client, ponsel) untuk menampilkan sesi virtual desktop. |

---

## 3. Protokol HDP (Huawei Desktop Protocol)
HDP adalah protokol transmisi desktop virtual milik Huawei yang dirancang khusus untuk efisiensi tinggi pada jaringan LAN maupun WAN:
- **Smart Text & Graphics Processing:** Memisahkan elemen teks, grafik vektor, dan gambar bitmap dalam satu frame layar untuk menerapkan kompresi lossless pada teks (tetap tajam) dan kompresi lossy adaptif pada gambar/video untuk menghemat bandwidth.
- **Video Acceleration:** Mendukung hardware decoding dan client-side redirection untuk streaming multimedia beresolusi tinggi (4K/60fps) dengan konsumsi CPU rendah.
- **Periferal Redirection Lengkap:**
  - **USB Redirection:** Perangkat USB fisik yang dicolokkan ke client di-passthrough ke virtual desktop (printer, scanner, flash drive, smart card reader).
  - **Device Mapping:** Pemetaan drive lokal, serial port, dan parallel port ke dalam sesi desktop.
  - **Clipboard Redirection:** Kontrol copy-paste teks dan file antara client lokal dan VM remote (dapat dibatasi unidirectional atau disabled untuk keamanan data).

---

## 4. Tipe Provisioning Virtual Desktop
1. **Linked Clone Desktop:**
   - Dibuat dari satu base template induk (Golden Image).
   - Setiap VM hanya menyimpan delta perubahan data uniknya pada disk terpisah (Delta Disk).
   - **Keuntungan:** Menghemat kapasitas storage hingga 70% - 80%, proses pembuatan batch desktop dalam hitungan menit, dan update patch OS dapat dilakukan terpusat dengan mengupdate base image saja.
2. **Full Copy Desktop:**
   - Setiap VM disalin secara utuh dari template awal dan memiliki virtual disk yang berdiri sendiri 100%.
   - **Kelebihan:** Pengguna memiliki hak penuh untuk memodifikasi OS tanpa terikat pada base image. Cocok untuk developer, analis, atau staf eksekutif.
3. **Full Memory Desktop (Memory-Based Desktop):**
   - Disk sistem VM dimuat langsung ke dalam RAM server fisik.
   - Menghasilkan performa IOPS super cepat dan latensi mendekati nol.
   - Cocok untuk skenario call center atau training lab yang tidak memerlukan retensi data lokal setelah user logout.

---

## 5. Mode Alokasi Desktop
- **Single User (Dedicated Desktop):**
  - Satu VM desktop didedikasikan secara permanen untuk satu akun pengguna spesifik.
  - Perubahan file, desktop wallpaper, dan aplikasi yang diinstal tetap tersimpan saat user logout atau reboot.
- **Dynamic Pool (Floating Desktop):**
  - Kumpulan sejumlah VM desktop dialokasikan secara dinamis ke sekelompok pengguna.
  - Pengguna mendapatkan VM mana saja yang sedang menganggur (idle) saat login, dan VM dikembalikan ke pool saat sesi berakhir. Sangat hemat lisensi dan sumber daya komputasi.
