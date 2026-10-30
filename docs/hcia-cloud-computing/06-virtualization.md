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
