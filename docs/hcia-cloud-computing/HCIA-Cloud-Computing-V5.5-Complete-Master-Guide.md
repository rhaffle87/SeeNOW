# HCIA-Cloud Computing V5.5 - Complete Master Handbook

Kompilasi Buku Panduan Lengkap Materi Kursus dan Sertifikasi Huawei HCIA-Cloud Computing V5.5 (Bab 01 sampai 14).

---

## Daftar Isi
1. [Chapter 01: Cloud Computing Basics](#chapter-01-cloud-computing-basics)
2. [Chapter 02: Server Basics & Hardware Architecture](#chapter-02-server-basics--hardware-architecture)
3. [Chapter 03: Storage Technology Basics](#chapter-03-storage-technology-basics)
4. [Chapter 04: Network Technology Basics](#chapter-04-network-technology-basics)
5. [Chapter 05: Operating System Basics](#chapter-05-operating-system-basics)
6. [Chapter 06: Virtualization](#chapter-06-virtualization)
7. [Chapter 07: Huawei Virtualization Platform (FusionCompute Architecture)](#chapters-06-07-08-virtualization--huawei-fusioncompute-platform)
8. [Chapter 08: Huawei Virtualization Platform Management and Usage](#chapter-08-huawei-virtualization-platform-management-and-usage)
9. [Chapter 09: Overview of FusionAccess Desktop Solution (VDI)](#chapters-09-10-11-12-huawei-fusionaccess-desktop-solution-vdi)
10. [Chapter 10: Planning and Deployment of FusionAccess](#chapter-10-planning-and-deployment-of-fusionaccess)
11. [Chapter 11: Service Provisioning of FusionAccess](#chapter-11-service-provisioning-of-fusionaccess)
12. [Chapter 12: Features and Management of FusionAccess](#chapter-12-features-and-management-of-fusionaccess)
13. [Chapter 13: Cloud Computing Trends & Emerging Technologies](#chapter-13-cloud-computing-trends--emerging-technologies)
14. [Chapter 14: HCIA-Cloud Computing V5.5 Lab Guide Summary](#chapter-14-hcia-cloud-computing-v55-lab-guide-summary)

---

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

---

# Chapter 02: Server Basics & Hardware Architecture

## 1. Jenis-Jenis Server Enterprise
- **Rack Server:** Bentuk modular standar rak 19 inci (satuan 1U, 2U, 4U). Fleksibel, pemeliharaan mudah, efisiensi pendinginan baik, paling banyak digunakan di data center cloud. Contoh: Huawei FusionServer Pro 2288H V5.
- **Blade Server:** Komputasi densitas sangat tinggi di mana server blade dimasukkan ke dalam chassis enclosure bersama yang berbagi power supply, kipas pendingin, dan modul switch jaringan. Menghemat kabel hingga 80%.
- **High-Density Server:** Menggabungkan kepadatan blade dengan fleksibilitas rack server untuk komputasi hyperscale cloud.

---

## 2. Komponen Perangkat Keras Utama Server
- **CPU (Central Processing Unit):**
  - **Arsitektur x86 (CISC):** Intel Xeon, AMD EPYC. Standar de-facto cloud komersial.
  - **Arsitektur ARM (RISC):** Huawei Kunpeng 920. Konsumsi daya rendah, efisiensi throughput multi-core tinggi.
- **Memori (RAM):**
  - Menggunakan modul ECC (Error-Correcting Code) DDR4 / DDR5 registered DIMM (RDIMM) untuk mendeteksi dan memperbaiki bit-flip error secara real-time demi stabilitas server 24/7.
- **Media Penyimpanan (Storage Drive):**
  - **SATA (Serial ATA):** Biaya murah, kapasitas besar, kecepatan 6 Gbps, untuk data arsip / cold data.
  - **SAS (Serial Attached SCSI):** Keandalan tinggi (MTBF tinggi), kecepatan 12 Gbps, transfer full-duplex untuk beban kerja enterprise.
  - **NVMe SSD (PCIe Bus):** Latensi ultra-rendah, throughput mencapai puluhan gigabit per detik via jalur bus PCIe langsung, untuk database dan high-performance storage pool.

---

## 3. Teknologi RAID (Redundant Array of Independent Disks)

| Tipe RAID | Minimum Disk | Pemanfaatan Kapasitas | Toleransi Kerusakan Disk | Karakteristik Performa |
|---|---|---|---|---|
| **RAID 0** | 2 | 100% ($N$) | 0 (Jika 1 rusak, semua data hilang) | Striping. Read & Write paling cepat, tidak ada redundansi. |
| **RAID 1** | 2 | 50% ($N/2$) | 1 disk | Mirroring. Keamanan tinggi, biaya storage per GB mahal. |
| **RAID 5** | 3 | $(N-1)/N$ | 1 disk | Distributed Parity. Keseimbangan terbaik antara biaya, kapasitas, dan keamanan. |
| **RAID 6** | 4 | $(N-2)/N$ | 2 disk | Dual Distributed Parity. Sangat aman, cocok untuk hard disk berkapasitas besar. |
| **RAID 10 (1+0)** | 4 | 50% ($N/2$) | 1 disk per mirror subgroup | Kombinasi Mirroring + Striping. Performa I/O tinggi dan redundansi maksimal. |

---

## 4. Manajemen Server Out-of-Band (Huawei iBMC)
- Menggunakan port jaringan fisik khusus (Management Port) yang terpisah dari port data produksi.
- Berjalan pada chipset BMC mandiri independen dari status OS utama server.
- **Fitur Utama iBMC:**
  - Remote KVM (Keyboard, Video, Mouse) dan Virtual Media redirection (mount file ISO jarak jauh).
  - Monitoring suhu, sensor voltase, dan status hardware komponen (CPU, RAM, Power Supply, Fan).
  - Kontrol daya jarak jauh (Power On, Power Off, Force Restart, Reset BIOS/IPMI).

---

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

---

# Chapter 04: Network Technology Basics

## 1. Model Referensi Jaringan (OSI 7 Layer vs TCP/IP)

| Layer OSI | Nama Layer | Protokol & Perangkat Terkait | Satuan Data (PDU) |
|---|---|---|---|
| **Layer 7** | Application | HTTP, HTTPS, DNS, DHCP, FTP, SSH | Data |
| **Layer 6** | Presentation | SSL/TLS, JPEG, ASCII, Kompresi | Data |
| **Layer 5** | Session | RPC, NetBIOS, Pemeliharaan Sesi | Data |
| **Layer 4** | Transport | **TCP** (Reliable, Three-Way Handshake) & **UDP** (Fast, Connectionless) | Segment |
| **Layer 3** | Network | **IP** (IPv4 / IPv6), ICMP, OSPF, BGP. **Perangkat:** Router, Layer 3 Switch | Packet |
| **Layer 2** | Data Link | Ethernet, 802.1Q VLAN, ARP, MAC Address. **Perangkat:** Layer 2 Switch | Frame |
| **Layer 1** | Physical | Kabel UTP RJ45, Fiber Optic, Hub, Transceiver | Bits |

---

## 2. Pengalamatan IP & Subnetting
- **Struktur Alamat IPv4:**
  - 32 bit bilangan biner, ditulis dalam 4 oktet desimal (contoh: `192.168.1.1`).
  - Terdiri dari dua bagian: **Network ID** dan **Host ID**, dipisahkan oleh **Subnet Mask**.
- **Rentang Alamat IP Private (RFC 1918):**
  - **Kelas A:** `10.0.0.0` - `10.255.255.255` (`10.0.0.0/8`)
  - **Kelas B:** `172.16.0.0` - `172.31.255.255` (`172.16.0.0/12`)
  - **Kelas C:** `192.168.0.0` - `192.168.255.255` (`192.168.0.0/16`)

---

## 3. Switching & VLAN (Virtual Local Area Network)
- **Fungsi Switch Layer 2:**
  - Meneruskan frame data berdasarkan tabel MAC address.
  - Tiga aksi forwarding switch: **Flooding** (broadcast/unknown unicast), **Forwarding** (known unicast), **Discarding** (filtering).
- **Konsep VLAN (IEEE 802.1Q):**
  - Mengisolasi broadcast domain pada level Layer 2 untuk meningkatkan keamanan dan efisiensi bandwidth jaringan.
  - Frame Ethernet ditambahkan Tag 802.1Q sebesar 4 byte yang berisi **VLAN ID** (rentang 1 - 4094).
- **Tipe Port Switch Huawei:**
  - **Access Port:** Menghubungkan switch ke perangkat akhir (PC, Server). Mengirim frame tanpa tag (untagged).
  - **Trunk Port:** Menghubungkan switch ke switch lain atau router. Mengizinkan lalu lintas banyak VLAN sekaligus (tagged).
  - **Hybrid Port:** Tipe port khas Huawei yang dapat mengonfigurasi beberapa VLAN tagged dan beberapa VLAN untagged sekaligus secara fleksibel.

---

## 4. Routing Basics
- **Routing:** Proses meneruskan paket data antar subnet/jaringan yang berbeda (Layer 3) berdasarkan tabel rute (Routing Table).
- **Rute Statis vs Rute Dinamis:**
  - **Static Routing:** Dikonfigurasi manual oleh admin. Hemat resource router, namun tidak adaptif terhadap perubahan topologi link failure.
  - **Dynamic Routing (OSPF - Open Shortest Path First):**
    - Protokol Link-State berbasis algoritma Dijkstra (SPF).
    - Menghitung jalur terbaik berdasarkan cost bandwidth antarmuka.
    - Cepat berkonvergensi saat ada kabel atau router yang putus.
    - Menggunakan pembagian Area (Area 0 / Backbone Area wajib ada).
- **Prioritas Routing Huawei (Preference Value - semakin kecil semakin diprioritaskan):**
  - Direct Interface: `0`
  - OSPF Internal: `10`
  - IS-IS: `15`
  - Static Route: `60`
  - RIP: `100`
  - OSPF ASE / External: `150`
  - BGP: `255`

---

# Chapter 05: Operating System Basics

## 1. Konsep & Peran Sistem Operasi (OS)
- **Definisi:** Perangkat lunak sistem mendasar yang menjembatani antara perangkat keras komputer (CPU, RAM, Disk, I/O) dan aplikasi pengguna.
- **Fungsi Utama OS:**
  1. **Manajemen Proses:** Penjadwalan alokasi siklus CPU ke thread/aplikasi (Preemptive multitasking).
  2. **Manajemen Memori:** Alokasi virtual address space, paging, swap, dan isolasi memori antar proses.
  3. **Manajemen File System:** Mengorganisasi penyimpanan file hierarki pada disk (NTFS, EXT4, XFS).
  4. **Manajemen Perangkat (I/O Device):** Komunikasi terstandarisasi dengan hardware menggunakan device driver.

---

## 2. Fondasi Sistem Operasi Linux (Huawei EulerOS)
- **Struktur Linux:**
  - **Kernel:** Inti sistem yang memiliki hak akses tertinggi (Ring 0 / Kernel Space).
  - **Shell:** Program antarmuka baris perintah (CLI seperti Bash) untuk menerima instruksi dari user.
  - **User Space Applications:** Program utilitas, daemon sistem (systemd), dan aplikasi bisnis (Ring 3).
- **Perintah Penting Administrasi Linux di Cloud:**
  - Status Resource: `top`, `htop`, `free -h`, `df -h`, `lsblk`.
  - Manajemen Jaringan: `ip addr`, `ip route`, `ping`, `ss -tulpn`, `traceroute`.
  - Manajemen Service: `systemctl status <service>`, `systemctl restart <service>`.
  - Hak Akses File: `chmod 755 <file>`, `chown root:root <file>`.

---

# Chapter 13: Cloud Computing Trends & Emerging Technologies

## 1. Cloud-Native & Containerization
- **Perbandingan Virtual Machine vs Container:**
  - **Virtual Machine (VM):** Memvirtualisasikan perangkat keras lengkap termasuk OS guest mandiri (kernel sendiri). Isolasi sangat kuat, namun ukuran image besar (gigabytes) dan boot-up butuh hitungan menit.
  - **Container (Docker):** Berbagi kernel OS host yang sama, mengisolasi aplikasi menggunakan Linux `cgroups` dan `namespaces`. Ukuran image sangat kecil (megabytes), startup dalam hitungan milidetik, densitas komputasi sangat tinggi.
- **Kubernetes (K8s):**
  - Standar industri untuk orkestrasi container terdistribusi: automated deployment, self-healing, auto-scaling, dan service discovery.

## 2. Serverless Computing
- Pengembang hanya menulis kode fungsi bisnis (Function-as-a-Service / FaaS).
- Penyedia cloud secara otomatis mengalokasikan server, mengeksekusi kode saat event terpicu, dan langsung mematikan resource saat selesai (*scale to zero*).
- Tagihan biaya hanya dihitung per milidetik eksekusi kode aktual.

## 3. Edge Computing & AI Cloud
- **Edge Computing:** Memproses data sedekat mungkin dengan sumber data (sensor IoT, gerbang pabrik, base station 5G) untuk memangkas latensi jaringan dan menghemat bandwidth uplink ke cloud pusat.
- **AI + Cloud:** Integrasi model machine learning skala besar langsung di data center cloud (seperti Huawei ModelArts) untuk akselerasi analitik dan kecerdasan artifisial terpusat.

---

# Chapter 06: Virtualization

## 1. Virtualization Overview
- **Karakteristik Utama Virtualisasi:**
  1. **Partitioning (Partisi):** Satu server fisik dapat dibagi menjadi beberapa mesin virtual (VM), di mana setiap VM menjalankan sistem operasinya sendiri.
  2. **Isolation (Isolasi):** Setiap VM terisolasi sepenuhnya. Crash, kebocoran memori, atau malware pada satu VM tidak mempengaruhi VM lain pada host fisik yang sama.
  3. **Encapsulation (Enkapsulasi):** Seluruh status VM (hardware virtual, konfigurasi, disk, memori) dikemas ke dalam beberapa file terpisah (seperti file `.vhd`, `.ovf`). Hal ini membuat VM sangat mudah di-backup, disalin, dan dipindahkan.
  4. **Hardware Independence (Independensi Perangkat Keras):** Sistem operasi guest tidak berinteraksi langsung dengan spesifikasi fisik hardware, melainkan dengan hardware virtual terstandarisasi yang disediakan oleh Hypervisor. VM dapat dipindahkan ke server fisik dengan vendor/tipe berbeda tanpa instalasi ulang driver.

---

## 2. Arsitektur Hypervisor & Mekanisme Virtualisasi
- **Hypervisor (VMM - Virtual Machine Monitor):**
  - Lapisan perangkat lunak yang mengontrol akses hardware fisik dan menyediakan abstraksi hardware untuk VM.
- **Tiga Dimensi Virtualisasi Komputasi:**
  1. **CPU Virtualization:**
     - **Full Virtualization:** Hypervisor menerjemahkan instruksi sensitif secara binary translation atau memanfaatkan akselerasi hardware (Intel VT-x / AMD-V) di Ring -1.
     - **Paravirtualization:** Kernel OS guest dimodifikasi untuk memanggil hypercall langsung ke hypervisor, meningkatkan efisiensi I/O.
  2. **Memory Virtualization:**
     - Pemetaan bertingkat: *Virtual Memory (VA) -> Guest Physical Memory (GPA) -> Host Physical Memory (HPA)*.
     - Menggunakan teknologi hardware EPT (Extended Page Tables) dari Intel atau NPT (Nested Page Tables) dari AMD untuk bypass overhead software shadow page table.
  3. **I/O Virtualization:**
     - **Emulasi Software:** Hypervisor mengemulasikan perangkat keras standar (seperti kartu jaringan Intel e1000 atau IDE controller). Kompatibilitas tinggi, performa sedang.
     - **Paravirtualized Driver (VirtIO):** Driver khusus di OS guest (seperti Huawei UVP Tools) yang berkomunikasi langsung dengan hypervisor melalui ring buffer. Performa mendekati *bare-metal*.
     - **Passthrough (SR-IOV / Direct I/O):** Hypervisor memberikan akses langsung ke kartu fisik PCI untuk satu VM tertentu. Performa tertinggi, latensi nol, namun tidak mendukung live migration.

---

## 3. Teknologi Hypervisor Populer di Industri
- **KVM (Kernel-based Virtual Machine):**
  - Modul virtualisasi open-source yang terintegrasi langsung ke dalam kernel Linux (`kvm.ko`).
  - Mengubah Linux menjadi Type 1 Bare-Metal Hypervisor.
  - Menjadi fondasi teknologi untuk Huawei FusionCompute UVP, OpenStack, dan Google Compute Engine.
- **Xen:**
  - Hypervisor Type 1 berbasis microkernel dengan konsep *Domain 0 (Dom0)* untuk kontrol manajemen dan *Domain U (DomU)* untuk VM guest.
- **VMware ESXi:**
  - Hypervisor Type 1 proprietary kelas enterprise terkemuka.

---

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

---

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

---

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

---

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

---

# Chapter 11: Service Provisioning of FusionAccess

## 1. Persiapan Template Desktop (Golden Image)
Template adalah cetak biru VM master yang digunakan untuk membuat puluhan hingga ribuan desktop virtual seragam:
1. **Pembuatan Base VM di FusionCompute:**
   - Spesifikasi vCPU, RAM, dan disk disesuaikan dengan kebutuhan pengguna (misal: Office Worker = 2 vCPU, 4GB RAM; Designer = 4 vCPU, 16GB RAM + vGPU).
2. **Instalasi Driver & Software Agen:**
   - Instal **Huawei UVP VM Tools** (driver paravirtualisasi storage dan network).
   - Instal **HDP Agent** (software komunikasi protokol desktop dengan HDC).
3. **Optimasi Sistem Operasi & Sysprep:**
   - Nonaktifkan service yang tidak diperlukan di lingkungan virtual (seperti disk defragmentation, indexing berlebih).
   - Eksekusi utilitas Windows `Sysprep` dengan opsi `/generalize /oobe /shutdown`.
   - *Tujuan Sysprep:* Menghapus Security Identifier (SID) unik mesin master agar saat di-clone, setiap VM mendapatkan SID baru yang unik di Active Directory domain.
4. **Konversi ke Template di VRM:**
   - Klik kanan VM yang sudah mati -> pilih *Convert to Template*.

---

## 2. Pembuatan Desktop Group di ITA
Desktop Group mengelompokkan VM desktop berdasarkan template, tipe provisioning, dan kebijakan akses yang sama:
- **Parameter Penentu Desktop Group:**
  - **Tipe Desktop:**
    - *Linked Clone Desktop:* Menggunakan base template induk + delta disk. Sangat efisien, hemat storage hingga 80%, update massal instan.
    - *Full Copy Desktop:* Setiap VM memiliki virtual disk independen 100%. Cocok untuk user VIP / custom developer.
    - *Full Memory Desktop:* Disk sistem dimuat langsung ke RAM fisik host untuk performa I/O ultra-tinggi.
  - **Tipe Alokasi User:**
    - *Single User (Dedicated):* 1 VM terikat permanen ke 1 user.
    - *Dynamic Pool (Floating):* Kumpulan VM digunakan bergantian oleh sekelompok user.
  - **Target Resource:** Memilih Cluster FusionCompute, Data Storage VIMS, dan Port Group VLAN untuk kartu jaringan desktop.

---

## 3. Proses Provisioning Otomatis
```
Admin ITA -> Create Desktop Group
    |
    v
ITA memanggil API FusionCompute VRM
    |
    v
VRM membuat VM-VM Linked Clone dari Template Master
    |
    v
VM dinyalakan otomatis -> Sysprep berjalan otomatis -> Bergabung ke Domain AD
    |
    v
HDP Agent di dalam VM terhubung ke HDC (Status: Ready / Unassigned)
    |
    v
ITA mengalokasikan VM ke User AD -> Status berubah menjadi "Assigned"
```
Pengguna sekarang dapat membuka browser atau HDP Client, login ke portal WI, dan langsung menggunakan desktop virtual miliknya.

---

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

---

# Chapter 13: Cloud Computing Trends & Emerging Technologies

## 1. OpenStack Overview
OpenStack adalah platform perangkat lunak open-source terkemuka di dunia untuk membangun dan mengelola cloud privat dan publik skala enterprise:

### A. Arsitektur Komponen Inti OpenStack
| Komponen | Nama Modul | Fungsi Utama dalam Cloud |
|---|---|---|
| **Keystone** | Identity Service | Autentikasi dan otorisasi terpusat, mengelola token akses, user, project/tenant, dan endpoint catalog service. |
| **Nova** | Compute Service | Mengelola siklus hidup mesin virtual (create, schedule, start, stop, migrate) di atas hypervisor (KVM, QEMU). |
| **Glance** | Image Service | Menyimpan, mengindeks, dan mendistribusikan image sistem operasi virtual (RAW, QCOW2, VHD, ISO). |
| **Neutron** | Networking Service | Menyediakan software-defined networking (SDN), IP management, virtual switch, router, firewall, dan floating IP. |
| **Cinder** | Block Storage Service | Mengelola persistent block storage (volume) yang dapat di-mount ke instance Nova (berbasis Ceph, iSCSI, FC). |
| **Swift** | Object Storage Service | Menyediakan penyimpanan objek terdistribusi berkapasitas masif yang tahan banting (skalabilitas PB/EB via HTTP API). |
| **Horizon** | Dashboard Service | Web GUI antarmuka pengguna grafis untuk mengelola seluruh resource OpenStack secara visual. |

---

## 2. Tren Teknologi Cloud Masa Kini

### A. Cloud-Native & Containerization (Docker & Kubernetes)
- **Container vs Virtual Machine:**
  - Container mengisolasi proses aplikasi pada level user space dengan berbagi kernel host yang sama menggunakan fitur Linux `cgroups` dan `namespaces`.
  - Memberikan densitas aplikasi 5x - 10x lebih padat dibanding VM konvensional dan waktu startup dalam orde milidetik.
- **Kubernetes (K8s):**
  - Standar orkestrasi container: automated rollouts/rollbacks, service discovery, load balancing, storage orchestration, self-healing, dan secret configuration management.

### B. Arsitektur Microservices & Serverless
- **Microservices:** Memecah aplikasi monolitik raksasa menjadi kumpulan layanan-layanan kecil independen yang berkomunikasi melalui API ringan (RESTful / gRPC).
- **Serverless (Function-as-a-Service / FaaS):**
  - Developer sepenuhnya terbebas dari manajemen infrastruktur, OS, atau VM.
  - Kode dieksekusi berdasarkan event trigger dan biaya dihitung murni per milidetik runtime.

### C. Edge Computing & AI Cloud Synergy
- **Edge Computing:** Menempatkan node komputasi di tepi jaringan (dekat sumber data IoT atau base station 5G) untuk memangkas latensi dari puluhan milidetik ke sub-milidetik.
- **AI Cloud:** Penyediaan infrastruktur komputasi akselerator terdistribusi (GPU / NPU Huawei Ascend) untuk pelatihan model bahasa besar (LLM) dan inferensi AI real-time secara terpusat.

---

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

---

