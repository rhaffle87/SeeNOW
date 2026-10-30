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
