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
