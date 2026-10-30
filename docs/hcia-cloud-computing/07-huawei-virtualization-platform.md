# Chapters 06, 07, 08: Virtualization & Huawei FusionCompute Platform

## 1. Virtualization Overview & Hypervisor Types
- **Konsep Inti:**
  - Virtualisasi adalah teknologi yang mengabstraksikan sumber daya fisik perangkat keras (CPU, memori, storage, network adapter) menjadi beberapa resource pool logis yang dapat dialokasikan ke banyak Virtual Machine (VM) independen.
  - **Perbedaan Virtualisasi vs Cloud Computing:**
    - Virtualisasi adalah **teknologi pendukung (enabler)** yang memecah resource fisik menjadi virtual.
    - Cloud Computing adalah **model bisnis dan operasional** yang mengemas resource tersebut menjadi layanan mandiri terukur (IaaS/PaaS/SaaS).
- **Klasifikasi Hypervisor:**
  - **Type 1 (Bare-Metal Hypervisor):**
    - Berjalan langsung di atas hardware fisik tanpa OS host perantara.
    - Performa tinggi, latensi rendah, efisiensi maksimal, standar enterprise data center.
    - Contoh: Huawei UVP (Unified Virtualization Platform), VMware ESXi, KVM (berjalan sebagai modul kernel Linux).
  - **Type 2 (Hosted Hypervisor):**
    - Berjalan di atas Operating System umum (seperti Windows atau Linux standar).
    - Performa lebih rendah karena ada lapisan overhead OS host.
    - Contoh: VMware Workstation, Oracle VirtualBox.

---

## 2. Arsitektur Huawei Virtualization Platform (FusionCompute)
FusionCompute adalah komponen virtualisasi cloud enterprise milik Huawei yang terdiri dari dua subsistem utama:

```
                    +--------------------------------+
                    |    VRM (Web GUI & REST API)    |
                    | (Management, Clustering, HA)   |
                    +---------------+----------------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
+---------v---------+                               +---------v---------+
|     CNA Node 1    |                               |     CNA Node 2    |
| +---------------+ |                               | +---------------+ |
| | VM1 | VM2 | VM3 |                               | | VM4 | VM5 | VM6 |
| +---------------+ |                               | +---------------+ |
| | UVP Hypervisor| |                               | | UVP Hypervisor| |
| +---------------+ |                               | +---------------+ |
| | Hardware x86  | |                               | | Hardware x86  | |
+-------------------+                               +-------------------+
```

### A. CNA (Compute Node Agent)
- Perangkat lunak virtualisasi yang diinstal langsung pada server fisik (bare-metal).
- Berbasis Linux EulerOS enterprise dengan kernel UVP (Unified Virtualization Platform).
- **Fungsi Utama CNA:**
  1. Menyediakan fungsi hypervisor untuk mengisolasi dan menjalankan VM.
  2. Melakukan virtualisasi CPU dan memori untuk VM.
  3. Mengelola virtual switch terdistribusi (OVS / Open vSwitch) untuk networking VM.
  4. Menerima dan mengeksekusi instruksi kontrol dari node VRM.

### B. VRM (Virtual Resource Manager)
- Node manajemen pusat untuk seluruh cluster virtualisasi FusionCompute.
- **Fungsi Utama VRM:**
  1. Manajemen siklus hidup VM (Create, Start, Stop, Pause, Delete, Snapshot, Clone).
  2. Manajemen resource pool komputasi, storage, dan network.
  3. Menjalankan algoritma penjadwalan resource dinamis (DRS) dan hemat daya (DPM).
  4. Memonitor status kesehatan host dan VM, serta mengeksekusi High Availability (HA) otomatis saat CNA failure.
  5. Menyediakan Web GUI portal terpadu dan antarmuka REST API untuk integrasi sistem eksternal.
- **Mode Deployment VRM:**
  - **VM Deployment:** VRM diinstal di dalam VM pada host CNA. Mendukung mode Active/Standby (dua VM VRM di dua host CNA berbeda) untuk redundansi tinggi.
  - **Physical Server Deployment:** VRM diinstal langsung pada server fisik khusus.

---

## 3. Fitur Utama & Mekanisme Kunci FusionCompute

### A. Virtualisasi Komputasi (Computing Virtualization)
- **CPU Virtualization:**
  - Berbasis hardware-assisted virtualization (Intel VT-x / AMD-V).
  - VCPU (Virtual CPU): Unit pemrosesan logis yang dialokasikan ke VM. Rasio overcommit vCPU:pCPU dapat diatur (misal 3:1 atau 5:1 tergantung beban kerja).
- **Memory Overcommitment (Teknologi Penghemat Memori):**
  - Mengizinkan total alokasi memori VM melebihi total RAM fisik server.
  - **3 Teknologi Overcommitment FusionCompute:**
    1. **Memory Ballooning:** Driver balon di dalam VM mengembang saat memori fisik host kritis, memaksa OS VM melepas memori idle kembali ke host.
    2. **Memory Swapping:** Memindahkan halaman memori VM yang jarang digunakan ke file swap pada storage sekunder.
    3. **Memory Sharing (KSM - Kernel Samepage Merging):** Menggabungkan halaman memori identik (read-only) dari beberapa VM ke satu frame fisik tunggal.

### B. Fitur Cluster Enterprise
- **HA (High Availability):**
  - Jika satu host CNA mati mendadak, VRM mendeteksi heartbeat yang hilang dan secara otomatis me-restart VM yang terkena dampak pada host CNA lain yang masih sehat di cluster yang sama.
- **DRS (Dynamic Resource Scheduler):**
  - Secara berkala memantau beban CPU dan memori setiap host dalam cluster.
  - Secara otomatis (atau rekomendasi ke admin) memigrasikan VM antar host menggunakan Live Migration untuk menyeimbangkan beban kerja.
- **DPM (Dynamic Power Management):**
  - Bekerja berdampingan dengan DRS. Saat beban cluster rendah (misal malam hari), VM dikonsolidasikan ke beberapa host saja, dan host CNA yang kosong dimatikan sementara via IPMI untuk menghemat konsumsi listrik.
- **Live Migration (Migrasi VM Tanpa Downtime):**
  - Memindahkan VM yang sedang aktif berjalan dari satu host CNA ke host CNA lain tanpa memutus sesi pengguna atau layanan jaringan.
  - Memori dipindahkan secara iteratif; saat perbedaan memori tinggal sedikit, VM di-suspend sekian milidetik untuk sinkronisasi akhir sebelum dipindah routing IP-nya.

### C. Storage Virtualization di FusionCompute
- **Tipe Data Storage:**
  - **Non-virtualized Storage:** Performa tinggi, format raw LUN, tidak mendukung disk thin provisioning lanjutan atau snapshot bertingkat cepat.
  - **Virtualized Storage:** Menggunakan sistem file cluster Huawei VIMS (Virtual Image Management System), mendukung thin provisioning, snapshot dinamis, dan kloning cepat.
  - **FusionStorage (Distributed Block Storage):** Menggabungkan disk lokal (SSD/HDD) dari setiap server menjadi satu pool SAN terdistribusi berkinerja tinggi.
- **Tipe Disk Provisioning:**
  1. **Thin Provisioning:** Alokasi kapasitas disk hanya sesuai data yang benar-benar ditulis saat itu. Menghemat ruang storage awal.
  2. **Thick Provisioning Lazy Zeroed:** Ruang disk dialokasikan penuh di awal, namun blok data hanya di-nol-kan (zeroed out) saat pertama kali ditulis.
  3. **Thick Provisioning Eager Zeroed:** Ruang disk dialokasikan penuh dan seluruh blok langsung di-nol-kan di awal pembuatan. Performa I/O paling optimal dan aman.

### D. Network Virtualization di FusionCompute
- **DVS (Distributed Virtual Switch):**
  - Switch virtual yang melintasi beberapa host CNA dalam cluster, menjamin konfigurasi port dan kebijakan VLAN identik di seluruh host.
- **Port Group:**
  - Kumpulan port virtual pada DVS yang berbagi konfigurasi atribut jaringan yang sama (VLAN ID, QoS limit, IP/MAC filtering).
- **Uplink:**
  - Port adapter fisik (NIC fisik server CNA) yang menghubungkan switch virtual DVS ke switch jaringan fisik di luar server (Top of Rack switch).
- **SR-IOV (Single Root I/O Virtualization):**
  - Memungkinkan satu kartu jaringan fisik membagi dirinya menjadi banyak Virtual Function (VF) independen yang langsung di-passthrough ke VM, memangkas overhead CPU hypervisor untuk kebutuhan throughput super tinggi.
