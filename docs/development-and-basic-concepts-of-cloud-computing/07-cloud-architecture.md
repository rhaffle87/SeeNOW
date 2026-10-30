# Chapter 07: Cloud Architecture

- **Deskripsi:** Lapisan Arsitektur Cloud (Hardware, Virtualisasi, Manajemen, Layanan)
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Cloud Architecture

Cloud Architecture

In last clip, we learned the following architecture. We call it a complete set of IT environment architecture, from resources to applications. Based on this, make some adjustments and refinements, then we can obtain the cloud computing architecture. This is a simple cloud computing architecture. How to understand it? We can compare the cloud architecture to a supermarket. If you want to open a supermarket, what's the first thing? You must have your commodities. The goods could be food, daily necessities, or some raw materials that needs to be processed. Then we need a place to store our goods. We'd better classify them so we can find them easily later. Supermarkets also need management platforms to make sure it's running properly and can make money. A back-end system and related employees are responsible for pricing the product, replacing expired goods, and repairing the cash register when something goes wrong. Finally, with these preparations, our supermarket can be open now. Our customers come to us and search for things on shelves, perhaps two hamburgers or three pillows, there are various types of sorted goods. Cloud architecture is similar to this. For the cloud, the goods of the supermarket correspond to the infrastructure of the cloud, and the warehouse of the supermarket corresponds to the resource pool of the cloud. The cloud also has a management platform. The official website of the cloud service provider is like the shelf at the top of the supermarket architecture. Let's go to each layer of the cloud architecture and briefly look at the content of each layer. First, the infrastructure layer consists of hardware devices, including computing, storage, network and security devices. Servers include x86 servers. And Huawei has TaiShan servers that use Kunpeng series processors of the ARM architecture, different from x86 ones. For storage, we have storage servers and distributed storage. A storage server has a dedicated chassis that can be connected to a disk enclosure with many hard disks. Distributed storage uses disks on different servers to form a distributed storage pool for data read and write. Network devices are mainly used for communication. The network connects servers and servers, servers and storage devices, as well as data centers and external networks. Security is also important. There are some security devices in the data center. At the resource pool layer, virtual computing resource pools, virtual storage resource pools, and virtual network resource pools are abstracted from physical infrastructure devices using virtualization technologies. On the upper part of the resource pool layer, usually there is a cloud resource management system. On the Huawei cloud platform, the resource pool layer uses FusionSphere OpenStack as the virtual resource scheduling system to integrate resources in physical data centers and to provide interfaces for the upper layer. FusionSphere OpenStack is a Huawei product that is enhanced based on open-source OpenStack for commercial use. For the third layer, the cloud management platform layer is responsible for O&M and operation. How to understand the two concepts? Simply put, O&M is "to live" and operation is "to live better". For supermarket, O&M means running properly while operation means making money. O&M ensures the continuous running of service systems. The key words are stability, security, reliability, infrastructure-oriented and software-oriented. The keywords of IT operation are experience, efficiency, and benefit, which are mainly business-oriented, service-oriented and people-oriented. On the basis of the preceding three layers, we can provide cloud services. Generally, a web page is used for customers to purchase cloud resources, just like supermarket shelves. Huawei provides more than 200 cloud service products of various types, For example ECS for compute, OBS for storage, GaussDB for Database. Just like the goods in our supermarket, if you are interested, visit the HUAWEI CLOUD official website www.huaweicloud.com for further learning. This is the main content of this course. Let's review the cloud computing architecture. It consists of four layers: infrastructure layer, resource pool layer, cloud management platform layer, and cloud service layer from bottom to top. Next section, we'll talk about some new technologies and how cloud computing support them.

---

### Modul: Quiz

随堂测验

5 /5

Unlimited

--