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
