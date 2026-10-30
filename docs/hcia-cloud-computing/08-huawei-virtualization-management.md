# Chapter 08: Huawei Virtualization Platform Management and Usage

Dokumentasi komprehensif untuk Chapter 08 kurikulum Huawei HCIA-Cloud Computing V5.5, mencakup manajemen platform dan penggunaan praktis fitur FusionCompute.

---

## 1. FusionCompute Computing Virtualization

### A. CPU Virtualization & QoS (Quality of Service)
Di FusionCompute, alokasi CPU fisik (pCPU/Core) ke Virtual CPU (vCPU) dikelola melalui hypervisor UVP dengan mekanisme QoS berikut:
1. **CPU Reservation (Reservasi CPU - MHz):**
   - Batas minimum daya pemrosesan CPU yang dijamin untuk VM tertentu.
   - Resource ini tidak dapat diambil oleh VM lain meskipun VM tersebut sedang idle.
2. **CPU Weight / Shares (Bobot CPU):**
   - Menentukan proporsi alokasi resource CPU antar-VM saat terjadi perebutan resource (contention).
   - Nilai default: High (2000), Medium (1000), Low (500).
   - Formula alokasi: $\text{Alokasi} = \frac{\text{Bobot VM}}{\sum \text{Bobot Semua VM}} \times \text{Kapasitas CPU}$.
3. **CPU Limit (Batas Maksimum CPU - MHz):**
   - Batas absolut pemakaian CPU yang diizinkan untuk sebuah VM, mencegah satu VM memonopoli seluruh CPU host.

### B. NUMA (Non-Uniform Memory Access) Node Architecture
- Pada server multi-socket (misal 2x atau 4x Intel Xeon/Kunpeng), setiap socket CPU memiliki kontroler memori lokal langsung.
- **Local Memory Access vs Remote Memory Access:**
  - Akses CPU ke memori lokalnya sendiri memiliki latensi paling rendah dan bandwidth tertinggi.
  - Akses ke memori di socket lain (remote) melalui interconnect bus (UPI/QPI) memiliki latensi lebih tinggi.
- **Optimasi NUMA di FusionCompute:**
  - Fitur **NUMA Node Pinning / Topology Awareness**: FusionCompute secara otomatis memetakan vCPU dan virtual RAM dari satu VM ke dalam satu NUMA node fisik yang sama untuk meminimalkan lintas-bus dan memaksimalkan performa.

### C. Memory Overcommitment Details
1. **Memory Ballooning:**
   - Driver `balloon.sys` di dalam VM bekerja sama dengan hypervisor.
   - Mengembang (*inflates*) untuk mengambil memori tak terpakai dari OS guest saat host butuh RAM, dan mengempis (*deflates*) saat guest membutuhkan kembali.
2. **Memory Swapping:**
   - Menggunakan file swap khusus pada datastore.
   - Hanya aktif jika ballooning tidak mencukupi untuk mencegah Out of Memory (OOM) crash pada host.
3. **Memory Sharing (KSM):**
   - Hypervisor memindai halaman memori 4KB yang identik antar-VM.
   - Halaman identik disatukan dan ditandai *Copy-on-Write (CoW)*. Saat ada VM yang menulis perubahan, hypervisor membuat salinan baru khusus untuk VM tersebut.

---

## 2. FusionCompute Storage Virtualization

### A. Arsitektur Storage FusionCompute
```
+--------------------------------------------------------------+
|                         Virtual Machine                      |
|                  Virtual Disk (.vhd / SCSI / IDE)            |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                         Data Storage                         |
|         Virtualized (VIMS)    |     Non-Virtualized (RAW)    |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                       Storage Resource                       |
|   IP-SAN (iSCSI) | FC-SAN | NAS (NFS/CIFS) | FusionStorage   |
+--------------------------------------------------------------+
                               |
                               v
+--------------------------------------------------------------+
|                     Physical Storage Devices                 |
|             Huawei OceanStor / Disk Array / Local SSD        |
+--------------------------------------------------------------+
```

### B. Tipe Data Storage: Virtualized vs Non-Virtualized
| Parameter | Virtualized Storage (VIMS) | Non-Virtualized Storage (Raw Device / LUN) |
|---|---|---|
| **Sistem File** | Huawei VIMS (Virtual Image Management System) | Tanpa sistem file cluster (Raw disk mapping) |
| **Thin Provisioning** | **Didukung penuh** (alokasi dinamis sesuai pemakaian data) | Tidak didukung (harus dialokasikan penuh di awal) |
| **Snapshot VM** | **Didukung penuh** (snapshot instan dan pohon snapshot bertingkat) | Terbatas atau tidak didukung pada level hypervisor |
| **Storage Live Migration** | **Didukung penuh** (pindah datastore tanpa mematikan VM) | Tidak didukung |
| **Overhead Performa** | Sangat kecil (optimal untuk 95% beban kerja enterprise) | Nol overhead (I/O langsung ke LUN fisik) |
| **Kasus Penggunaan Utama**| VM general-purpose, VDI, web server, application server | Database performa ekstrem (Oracle RAC, SQL Server Cluster) |

### C. Mode Disk Virtual di FusionCompute
1. **Independent & Persistent:**
   - Data ditulis langsung ke disk dan **tidak terpengaruh oleh snapshot VM**.
   - Saat VM di-restore ke snapshot lama, data pada disk ini tetap utuh (cocok untuk partisi database transaksi atau data log).
2. **Independent & Non-Persistent:**
   - Perubahan data disimpan sementara. Begitu VM dimatikan (*power off*) atau di-restart, **seluruh perubahan data hilang kembali ke kondisi awal**.
   - Cocok untuk VM kios publik, lab ujian, atau internet cafe.
3. **Dependent (Default):**
   - Disk ikut disertakan dalam snapshot VM. Saat snapshot di-revert, data pada disk ini kembali ke kondisi saat snapshot diambil.

### D. Multi-Pathing (UltraPath)
- Menggunakan beberapa jalur kabel fisik (HBA / NIC) antara host CNA dan storage array.
- **Failover:** Jika satu switch FC atau kabel putus, traffic I/O otomatis beralih ke jalur cadangan tanpa interupsi.
- **Load Balancing:** Membagi beban I/O secara merata ke seluruh link aktif.

---

## 3. FusionCompute Network Virtualization

### A. Komponen Jaringan Virtual
- **DVS (Distributed Virtual Switch):**
  - Mengabstraksikan switch di banyak host CNA menjadi satu kesatuan logis terpusat.
  - Memastikan konfigurasi network (VLAN, Port Group, QoS) konsisten saat VM berpindah antar-host.
- **Port Group (Grup Port):**
  - Titik koneksi virtual network adapter (vNIC) milik VM ke DVS.
  - Setiap Port Group memiliki konfigurasi:
    - **VLAN ID:** Menentukan segmentasi jaringan Layer 2.
    - **Traffic Shaping (QoS):** Membatasi bandwidth puncak (Peak Bandwidth), rata-rata (Average Bandwidth), dan burst size.
    - **Security Policy:** IP/MAC filtering, DHCP trust policy, pencegahan IP spoofing.
- **Uplink:**
  - Menghubungkan DVS ke kartu jaringan fisik (pNIC) host CNA.
  - Mendukung NIC bonding mode: **Active/Standby** atau **Load Balancing (IP Hash / LACP)**.

### B. Alur Paket Data VM-to-VM (Data Forwarding Path)
1. **Komunikasi VM dalam Host yang Sama & Port Group yang Sama:**
   - Paket diteruskan langsung oleh switch internal kernel (OVS) pada host CNA tanpa keluar ke kartu jaringan fisik.
2. **Komunikasi VM Antar-Host yang Berbeda:**
   - vNIC VM1 -> Port Group DVS -> Uplink pNIC host 1 (diberi Tag VLAN) -> Switch fisik (Trunk) -> Uplink pNIC host 2 (Tag VLAN diverifikasi) -> Port Group DVS -> vNIC VM2.
3. **Komunikasi Antar-VLAN Berbeda:**
   - Membutuhkan perangkat Layer 3 (Router fisik, Layer 3 Switch, atau Virtual Router) untuk melakukan inter-VLAN routing.

---

## 4. FusionCompute Virtualization Platform Management

### A. Manajemen Siklus Hidup VM (VM Lifecycle)
- **Pembuatan VM:**
  - Metode: Pembuatan manual baru, kloning dari VM aktif, konversi dari Template, atau import file OVF/OVA.
- **Template Management:**
  - Mengonversi VM yang sudah terkonfigurasi (OS + tools + patch) menjadi Template *read-only*.
  - Template digunakan untuk membuat puluhan/ratusan VM baru secara identik dalam hitungan menit.
- **VM Snapshot:**
  - Menyimpan status memori, konfigurasi, dan delta disk pada waktu tertentu (*point-in-time*).
  - Digunakan sebelum melakukan upgrade software atau patch OS yang berisiko tinggi.
  - *Catatan Penting Ujian:* Snapshot **bukan** pengganti backup jangka panjang karena snapshot bertingkat yang menumpuk akan menurunkan performa I/O disk.

### B. High Availability (HA) Cluster Mechanism
```
Host CNA 1 (Faulty)                       Host CNA 2 (Healthy)
+-----------------------+                 +-----------------------+
|  VM-A (Mati Mendadak) |                 |                       |
+-----------------------+                 +-----------------------+
           |                                          ^
           | Detak Jantung Hilang (Heartbeat Lost)    |
           v                                          |
+-----------------------------------------------------+-----------+
|                          VRM Management Node                    |
|   1. Deteksi host failure via Management Network & Storage Ping |
|   2. Isolasi Host CNA 1 (Fencing)                               |
|   3. Perintahkan Host CNA 2 me-mount VIMS datastore VM-A        |
|   4. Boot ulang VM-A otomatis di Host CNA 2                     |
+-----------------------------------------------------------------+
```
- **Kondisi Syarat HA:**
  1. Datastore tempat disk VM berada harus berupa **Shared Storage** yang dapat diakses oleh kedua host CNA.
  2. Kedua host CNA harus berada dalam satu Cluster yang sama dengan opsi HA diaktifkan.
  3. Destination host harus memiliki sisa kapasitas CPU dan RAM yang cukup.

### C. Dynamic Resource Scheduling (DRS) & Dynamic Power Management (DPM)
- **DRS (Dynamic Resource Scheduler):**
  - Mencegah *hotspot* (satu host overloaded sementara host lain nganggur).
  - Menggunakan algoritma penjadwalan beban periodik (default interval: 5 menit).
  - Mode DRS:
    - **Automated:** FusionCompute langsung mengeksekusi live migration VM secara otomatis saat ambang batas terlampaui.
    - **Manual:** FusionCompute memberikan daftar rekomendasi migrasi ke admin di Web GUI untuk disetujui.
- **DPM (Dynamic Power Management):**
  - Syarat wajib: Server fisik harus mendukung kartu IPMI / iBMC dan DRS aktif.
  - Di malam hari / saat utilisasi cluster rendah: DRS memadatkan VM ke host 1 dan 2, lalu DPM mematikan host 3 via remote IPMI command.
  - Di pagi hari / saat traffic naik: DPM mengirim sinyal Wake-on-LAN / IPMI Power On untuk menyalakan kembali host 3.

### D. VM Live Migration (vMotion)
- **Komponen yang Dipindahkan:**
  1. **Status Memori:** Hypervisor menyalin memori VM dari host sumber ke host tujuan secara berulang (iteratif). Halaman memori yang berubah selama proses (*dirty pages*) dikirim pada iterasi berikutnya.
  2. **Status Device:** Register CPU dan status interupsi virtual disinkronkan.
  3. **Switch Sesi:** VM di-suspend sekian milidetik, switch final dilakukan, dan host tujuan mengirim paket *Gratuitous ARP (GARP)* ke switch fisik agar tabel MAC beralih ke port host baru.
- **Syarat Live Migration:**
  - Arsitektur CPU host sumber dan host tujuan harus kompatibel (sama-sama Intel atau sama-sama AMD/Kunpeng).
  - Shared Storage dapat diakses oleh kedua host.
  - Port Group jaringan yang sama tersedia di host tujuan.
