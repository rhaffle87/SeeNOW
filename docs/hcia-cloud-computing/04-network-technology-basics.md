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
