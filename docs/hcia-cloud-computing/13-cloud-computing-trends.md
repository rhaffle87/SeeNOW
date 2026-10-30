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
