# Development and Basic Concepts of Cloud Computing - Master Handbook

Buku Panduan Lengkap Materi Kursus Resmi Huawei: **Development and Basic Concepts of Cloud Computing** (Chapter 01 sampai Chapter 10).  
Sumber Resmi: `https://e.huawei.com/en/talent/outPage/#/sxz-course/home?courseId=edxr72w_SgSdvaa6Cp8Xxkgd6bM&pageType=learn&operate=1`

---

## Daftar Isi Bab
1. [Chapter 01: Cloud is Already Here with You](#chapter-01-cloud-is-already-here-with-you)
2. [Chapter 02: Advantages of Cloud](#chapter-02-advantages-of-cloud)
3. [Chapter 03: Definition of Cloud](#chapter-03-definition-of-cloud)
4. [Chapter 04: Origin and Development](#chapter-04-origin-and-development)
5. [Chapter 05: Deployment Models](#chapter-05-deployment-models)
6. [Chapter 06: Service Models](#chapter-06-service-models)
7. [Chapter 07: Cloud Architecture](#chapter-07-cloud-architecture)
8. [Chapter 08: Cloud: Enabler of New Techs](#chapter-08-cloud-enabler-of-new-techs)
9. [Chapter 09: Cloud Trends](#chapter-09-cloud-trends)
10. [Chapter 10: Master Terminology & Course Summary](#chapter-10-master-terminology--course-summary)

---

# Chapter 01: Cloud is Already Here with You

- **Deskripsi:** Pengenalan Keberadaan Cloud di Kehidupan Sehari-hari
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Cloud is Already Here with You

Cloud is Already Here with You

Nowadays, everyone talks about “Cloud”, “5G", “AI”. Since cloud computing is such a hot topic, what is cloud computing? Where is the cloud? Actually, cloud computing is already here with you. Most of the apps we use in our daily life rely on cloud computing. Take Google Translate as an example, it has a simple user interface, but provides powerful performance. This depends on powerful servers in the cloud. With a lightweight APP and powerful cloud computing capabilities in the background, the accuracy of translation is guaranteed. And cloud storage, like Google Drive, iCloud and Dropbox, is another type of cloud service. We can upload local files to the cloud for storage and backup. Another example is cloud conferencing. With cloud conference, we can quickly and efficiently share voice, videos and data files with teams and customers around the world. Currently, cloud computing has been widely used in e-commerce, education, healthcare, transportation, government, gaming, airport, bioscience, automobile and other industries, everywhere. We live in the world of cloud computing. Cloud computing is the present and the future. In this course, we will demystify cloud computing, help you understand its advantages, concepts, history, models and trend. We will also introduce some other technologies that reforming the world with cloud, and how cloud support them. Then let's start our learning journey.

---

### Modul: Outline

Outline

---

# Chapter 02: Advantages of Cloud

- **Deskripsi:** 5 Keunggulan Utama Cloud Computing & Istilah Terkait (OBS, EIP)
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Advantages of Cloud

Advantages of Cloud

图文标题

Why is cloud computing more and more popular? What are the advantages of cloud computing? Now let’s have a look. Generally, cloud computing has five advantages. They are on-demand self-service, broad network access, resource pooling, rapid elasticity and measured service. The first is on-demand self-service. It means that you can purchase different types and quantities of services according to your needs. Usually, cloud service providers have their own service catalogs. You only need to select desired resources’ type and quantity, add them to the shopping cart, and pay for them just like shopping on a shopping website. The whole process is efficient and convenient with low communication costs. The second advantage is broad network access. It means that you can get your service wherever you are and whenever you are. Imagine that you have purchased storage space to store your photos and you can easily obtain them wherever you go. The only thing you need is internet access, whether it's fiber optic, Wi-Fi or cellular network. The third advantage is resource pooling. Imagine that you're in the cafeteria and want a coke. You might buy a bottled Coke or grab a cup and get it from the soda fountain. A bottled cola, which is similar to the traditional device usage model, you buy it then drink it alone. While a soda fountain is a resource pool, which can be shared by multiple people. Just like in cafeteria, we have not only coke, but orange juice, beer, etc. Cloud computing resource pools also have resources of the same type grouped together, including computing, storage and network etc. Resource pooling has two benefits: one is resource aggregation, unified management and control; the other is fine-grained and flexible division. The fourth is rapid elasticity. Elasticity refers to elasticity in obtaining and releasing cloud computing resources. Enterprises can quickly obtain required resources for service deployment. Resources can be flexibly scaled. For example, on shopping festivals such as Black Friday, e-commerce enterprises have to bear much more pressure than usual. In such cases, additional cloud computing resources can be quickly obtained to support the service and then released after peak hours. Enterprises only need to pay for the resources they use instead of purchasing additional infrastructure. Thus the cost is lower and service deployment is faster. The last one is measured services. Services in cloud computing can be measured based on the usage time, resource quota, and traffic. Customers can clearly view the usage of purchased services, analyze the used resources, and optimize the configuration to purchase more or degrade some. They can also precisely pay for the resources they use and know what resources they are paying for and for which period. These are the five advantages of cloud computing. Cloud computing makes it easier and cost-effective for enterprises to acquire IT infrastructure resources and technical support .This allows enterprises to focus more on business innovation. On-demand self-service, broad network access, resource pooling, rapid elasticity and measured service.  These are the five advantages of cloud computing. They make cloud computing more and more significant in enterprise strategic planning and implementation. And cloud computing is an important reality in today’s IT world. That´s all for this class. In the next lesson, we will elaborate what’s cloud computing, See you.

---

### Modul: Terminology

Full name

Description

OBS

Object Storage Service

An object-based cloud storage service. It provides data storage of easy extensibility, high security, proven reliability, and high cost efficiency.

EIP

Elastic IP Address

The Elastic IP Address (EIP) service provides independent public IP addresses and bandwidth to the Internet. An EIP can be flexibly associated with or disassociated from an ECS, BMS, virtual IP address, load balancer, or NAT gateway. Various billing modes are provided to meet diversified service requirements.

---

### Modul: Quiz

随堂测验

5 /5

Unlimited

--

---

# Chapter 03: Definition of Cloud

- **Deskripsi:** Definisi Formal Cloud Computing & Model Alokasi Sumber Daya
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Definition of Cloud

Definition of Cloud

In the previous lesson, we learned five advantages of Cloud computing: on-demand self-service, broad network access, resource pooling, rapid elasticity and measured service. Now, we will learn the definition of it. According to the National Institute of Standards and Technology(NIST), cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources, such as networks, servers, storage, applications, and services, that can be rapidly provisioned and released with minimal management effort or service provider interaction. This definition is very long, and we can grasp three keywords to understand it. First keyword: network. Networks are indispensable to cloud computing. A complete cloud computing environment consists of the cloud, networks, and terminals. The cloud refers to where we complete our computing tasks. Generally, this place is a data center equipment room where many servers process data. The terminal is an input/output device. The computer network connects the cloud to the terminal to transmit information – it transmits instructions input from the terminal to the cloud, and returns the execution result to the terminal, just like a pipe. Second: resources. As the definition says, cloud computing resources include computing, storage, network, applications, and services etc. Resource features are pooled, configurable, and can be quickly provided and released. Third: Services. For example, when you're going out, you can buy a car or take an Uber. Buying a car is on-premises, while the Uber solution is a service. You do not buy a car from Uber, but pay for the service that Uber moves you from place A to place B. Cloud computing provides cloud resources to customers as services. Customers do not actually own devices in equipment room of cloud vendors such as HUAWEI, but use some to process services. This is similar to leasing. In general, cloud computing means moving the computing process from the local computers to the remote servers. We do not need to care about the specific equipment room and device, just like a cloud in the sky. Cloud is a metaphor for networks. Underlying details are omitted. Computing is like a computer, powerful enough to provide computing, storage, and other services. "Cloud computing" can be understood as a model providing services to users by using computers that are powerful enough to provide them over the Internet. That‘s all for today, we learned the definition of cloud computing. In the next lesson, we will talk about the origin and development of cloud computing.

---

### Modul: Quiz

随堂测验

5 /5

Unlimited

--

---

# Chapter 04: Origin and Development

- **Deskripsi:** Sejarah & Evolusi Komputasi (Mainframe, PC, Internet, Broadband)
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Origin and Development

Origin and Development

From the definition in the previous section, we already know that cloud computing moves the processing process that was originally local to the remote end and then sends the results back. Therefore, cloud computing originates from the development of networks and the transformation of computing. First, let's look at the development of networks. In the early days, computers were huge and expensive. People wanted to communicate and share resources with computers in other regions. ARPANET was born in 1969. It was the precursor of the Internet. Later, more computers around the globe were connected. In the 1990s, Tim Berners Lee led the World Wide Web project, which became the www in front of our website. Meanwhile, Amazon and Google were established. After the millennium, network connections and traffic boomed. Facebook was founded in 2004. More and more people became Internet players. The bandwidth and speed of the network have been improved continually. Then let's review the development of computing. Here we focus on virtualization, which is a core technology of cloud computing. In the mainframe age, computing resources were quite limited. In 1955, John McCarthy proposed the theory of sharing computing time among users.10 years later, IBM launched the Time Sharing System (TSS). In 1999, VMware launched software that can implement virtualization on the x86 platform. This is important, because before that virtualization was a game of mainframes, while over decades, Intel's x86 architecture PCs and servers had become the mainstream. In the next ten years, multiple commercial or open-source virtualization software appeared such as VMware ESX, the predecessor of ESXi，Microsoft Hyper-V and Xen, KVM. If only virtualization technology is applied, the current cloud computing will not be available. What is more important is to combine virtualization and network to share computing resources, forming a business model that can generate huge economic benefits. Amazon was the pioneer. In 2006, AWS launched the first cloud products, Simple Storage Service (S3) and Elastic Compute Cloud (EC2), enabling enterprises to use AWS infrastructure to build their own applications. Then more tech giants launched their own cloud platforms and products. The cloud computing business model has been recognized in the market. More and more users accept and use cloud computing service and the industry chain has started to develop and integrate. Then, the emergence of OpenStack makes heterogeneous platform management more intelligent. And docker has made virtualization more lightweight. VMs has been gradually replaced by containers. Cloud computing entered the container era. From the birth of cloud computing to today, Cloud computing evolution has three milestones. In the cloud computing 1.0 era, computing virtualization is the core. More IT applications exist on fewer computing nodes to improve resource utilization. Then, next era features “software-defined" and integration. We concentrate on resource servitization and management automation. In the 3.0 era, the key words are "cloud native" and "APP redesign", cloud computing focuses on cloud-native and service reconstruction, bringing enterprise services to a new level in intelligence, agility, and efficiency improvement. Today, with multiple advantages, cloud computing supports the development and innovation of multiple industries and technologies. In this class, we have learned the origin and development of Cloud Computing, cloud computing is still evolving and is promising in the future. Next, we will talk about Cloud computing deployment models.

---

### Modul: Terminology

Term

Full name

Description

ARM

Advanced Reduced Instruction Set Computing Machines

Reduced instruction set computing, is a CPU design strategy based on the insight that a simplified instruction set provides higher performance when combined with a microprocessor architecture capable of executing those instructions using fewer microprocessor cycles per instruction. A computer based on this strategy is a reduced instruction set computer.

VMware

/

A leader in virtualization technology. VMware provides a portfolio of software products for virtualizing hardware resources to enable one physical server to take the role of multiple servers.

X86

/

x86 is the generic name for Intel processors released after the original 8086 processor.

OpenStack

/

OpenStack is a free and open-source software platform for cloud computing, mostly deployed as Infrastructure as a Service (IaaS), whereby virtual servers and other resources are made available to customers. The software platform consists of interrelated components that control diverse, multi-vendor hardware pools of processing, storage, and networking resources throughout a data center.

Docker

/

The term docker can refer to The Docker project as a whole, which is a platform for developers and sysadmins to develop, ship, and run applications the docker daemon process running on the host which manages images and containers

VPN

Virtual Private Network

The term describes any technology that can encapsulate and transmit network data, typically Internet Protocol data, over another network. Such a system enables users to access network resources that may otherwise be inaccessible from the public internet.

DNS

·        Domain Name Server

A functional entity in the TCP/IP network. With deployment of the DNS, subscribers can access related servers using corresponding domain names. In the TCP/IP network, a domain name maps an IP address. Domain names are easier to remember but servers in the network communicate with each other using IP addresses. Therefore the DNS is used to convert domain names to corresponding IP addresses.

TCP/IP

Transmission Control Protocol/Internet Protocol

Common name for the suite of protocols developed to support the construction of worldwide internetworks.

WWW

·        World Wide Web

A large scale hypermedia information system that allows users to browse information.

ESXi

/

A virtualization platform for creating and running virtual machines. ESXi virtualizes processor, memory, and storage resources and allocates the resources for virtual machines. Virtual machines, operating systems, and applications can run above the ESXi.

Xen

Xen is a Hypervisor providing services that allow multiple computer operating systems to execute on the same computer hardware concurrently.

KVM

·        Kernel-based Virtual Machine

Kernel-based Virtual Machine (KVM) is a virtualization infrastructure for the Linux kernel. KVM requires a processor with hardware virtualization extension.

LXC

Linux Container

LXC (Linux Containers) is an operating-system-level virtualization method for running multiple isolated Linux systems (containers) on a control host using a single Linux kernel.

Hyper-V

/

A VM system provided by Microsoft, which is installed on hosts.

EC2

Elastic Compute Cloud

Amazon Elastic Computing Cloud (Amazon EC2) is a web service provided by Amazon. It enables users to rent cloud computers to run required applications.

S3

Simple Storage Service

Amazon Simple Storage Service is storage for the Internet. It is designed to make web-scale computing easier for developers.

---

### Modul: Quiz

随堂测验

10 /10

Unlimited

--

---

# Chapter 05: Deployment Models

- **Deskripsi:** 3 Model Deployment: Public Cloud, Private Cloud, Hybrid Cloud
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Deployment Models

Deployment Models

Welcome back. After we learned about the history and evolution of cloud computing, we'll focus on the deployment models of cloud computing in this section. The three most common cloud computing deployment models are public cloud, private cloud, and hybrid cloud. Here is a simple metaphor to understand. Alice, she puts a safe at home to keep all her property. And this way is like a private cloud. While for Bob, there's no safe. He puts his property in the bank, like a public cloud. For Carol, she puts some money in her own safe, and the rest in the bank, like a hybrid cloud model. Their money can be seen as enterprise’s service and data, and safe is cloud infrastructure. Their houses are firewalls of enterprises, while the bank is just like a cloud vendor providing services to the public. For example, Amazon AWS，Microsoft Azure, HUAWEI ClOUD. In general, the difference lies in whether data and services are deployed inside or outside the enterprise firewall. Now we have three models, which one should we choose? Actually, the answer depends on service requirements and scenarios. Let's discuss pros and cons of them. For public cloud, it is a model in which resources, such as applications and storage, are prepared by cloud vendors, then and the public can access them through the network. Public cloud services can be free of charge or pay-per-use, and it is the most popular one. No investments are required to deploy and maintain the IT infrastructure. It provides powerful resource flexibility and agility. For enterprises, the capital expenditure (CAPEX) can be converted into operating expense (OPEX) to shorten the return on investment. The advantages of the public cloud are low costs and excellent scalability. As the data volume increases, the capacity can be expanded continuously. But due to the lack of control over cloud resources, security issues of confidential data, network performance, and compatibility issues maybe bottlenecks. Many customers worry about the security of public cloud. Actually, for small and medium-sized companies, the risks of data leakage and service interruption when adopting public cloud are far less than those of using their own equipment rooms. Some enterprises, such as those in the financial industry, cannot afford the risk of any data loss or leakage. Or facing the situation that some critical services, can't be migrated to the public cloud. Building their own private clouds can be a better choice. The private cloud refers to cloud solution that is used exclusively by an organization. Private clouds can be built by enterprise IT departments or cloud platform service providers. Usually the data center resources are located on-premises. The computing resources are not shared with other customers, but just kept inside the organization. Private cloud can effectively control data confidentiality, data security, and service quality. Private clouds are good choices for enterprises that have high requirements on data security and stability. However, all hardware, software, and security resources must be purchased by themselves, which is costly. And it takes a long time to deploy it. In addition, professional maintenance teams are required in the company. Here is a brief contrast between Public and Private cloud. Hybrid cloud is a combination of the above two. It integrates the convenience and cost-effectiveness of public cloud with the security and stability of private cloud. Enterprises who want to store data on private clouds and use resources of public clouds at the same time, can use public clouds and private clouds in a hybrid manner. Sensitive data or critical workloads can be stored on private clouds, while common or extended workloads can be stored on public clouds. Or they can use a private cloud environment to handle their daily IT workloads and use public cloud resources to supplement the infrastructure to accommodate occasional surges in network traffic. Everything comes with limitations. The hybrid cloud draws on the advantages of public and private clouds, but the complexity is also greatly increased, requiring strong compatibility and integration between cloud infrastructures across different locations and categories. It’s hard to manage. And as organization operations and management evolves, the combination of private and public cloud complicates the architecture. This is all about this part. We mainly introduced the concepts of public, private and hybrid cloud, and their pros and cons. Have you got it? In the next section, we will learn three service models of cloud computing: IaaS, PaaS and SaaS.

---

### Modul: Terminology

Term

Full name

Description

CAPEX

Capital Expenditure

Capital expenditures (CAPEX or capex) are expenditures creating future benefits. A capital expenditure is incurred when a business spends money either to buy fixed assets or to add to the value of an existing fixed asset with a useful life that extends beyond the taxable year.

OPEX

Operating Expense

An operating expense, operating expenditure, operational expense, operational expenditure or OPEX is an ongoing cost for running a product, business, or system.

TCO

Total Cost of Ownership

Total cost of ownership (TCO) is a financial estimate whose purpose is to help consumers and enterprise managers determine direct and indirect costs of a product or system. It is a management accounting concept that can be used in full cost accounting or even ecological economics where it includes social costs.

---

### Modul: Quiz

随堂测验

10 /10

Unlimited

--

---

# Chapter 06: Service Models

- **Deskripsi:** Model Layanan Cloud: IaaS, PaaS, SaaS, dan XaaS
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Service Models

Service Models

In the last class, we learned about the concepts of public, private and hybrid cloud, and their pros and cons. And we mentioned that one of the key words of cloud computing is service in the definition section. Cloud computing resources are provided for users in the form of services. Today，we will discuss cloud service models. Here are three cloud service models based on the resource levels: Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS). For ease of memory, they can be refined into SPI. There are some other aaS models, such as DaaS (Data as a service), STaaS (Storage as a Service), BaaS (Backend as a Service), which are classified by resource type. Everything can be a service. Let's go back to the "SPI". What are they, and what's the difference? There is a classic analogy called "Pizza as a Service" as a visualization of the differences among these concepts. Imagine that you want to enjoy a pizza. You can make your own pizza from scratch. There's a lot of stuff to be prepared, including pizza ingredients, oven, gas and even a table to put your pizza when you eat. That’s really a hassle. Or you can ask for help, or, in other words, use services provided by others. You have three options. They are take & bake，pizza delivered or dining out. For the first option, you need to buy an uncooked pizza from the pizzeria, bake it at home, and eat it at your own table. Unlike doing it yourself at home, you need a pizza vendor. For pizza delivered, with just one call, then pizza's on the doorstep. For dinning out, you don't have to prepare anything. The three solutions can be summarized as above. They are similar to IaaS, PaaS, and SaaS of cloud computing. This is the case with cloud computing. From bottom to top, this is a complete set of IT environment from underlying resources to applications. We can see computing, storage, network resources, and virtualization. These belong to infrastructure. The OS is the operating system. And the middleware and runtime environment are used by developers. Data and applications are the last step. If an enterprise wants to bring a service online without relying on external resources, it has to prepare all these resources. But now that we have cloud services, things are much easier. We can use resources provided by cloud service providers. If we use their infrastructure, it is IaaS. If the running environment is ready, it is PaaS. If we directly use software developed by them, it is SaaS. From left to right, the workload is decreasing，which is blue part in the preceding figure. IaaS > PaaS > SaaS. With more resources provided by cloud service providers, our investment in management and development is less, and the level of customization is reduced as well. IaaS is the bottom layer of cloud services and provides basic resources. IaaS is the bottom layer of cloud services and provides basic resources. Users need to manage their cloud servers and data, and design how to interconnect cloud servers. For example, ECS, EVS, VFW on HUAWEICLOUD. For Startups and small companies, they may pick IaaS to avoid spending too much time and money on purchasing and managing hardware and software when budgets are limited. Enterprises can also take the advantage of IaaS services to implement elastic scaling of basic resources and to cope with traffic peaks. PaaS provides an online platform that's accessible to different users, mainly developers. These platforms can be adopted for software development, IoT backend system, business analytics/intelligence, or some other uses. Cloud vendors help manage the underlying infrastructure, dev tools, runtime, database and so on. This spares users from troublesome business like deploying physical resources, and installing various development tools. They can focus on their own business logic. Typical PaaS platforms include Google App Engine and OpenShift. PaaS services can greatly reduce costs and accelerate deployment when you are developing an application. SaaS is a model that software development, deployment, and management, are all handed over to a third party. Therefore, you do not need to pay attention to technical issues and can use the software as you want. Almost all we access are SaaS services, such as Salesforce, Google Apps, Dropbox, Facebook, Twitter, and Instagram. For enterprises, they can also benefit from SaaS. For example, if a company need Customer Relationship Management (CRM) system, they may turn to Salesforce. By choosing one of the different plans and subscribe to the system, then they can create greater value for more customers. Compared with traditional self-developed software by enterprises, SaaS can help enterprises save cost, improve efficiency and create value. These are three service models of cloud computing: IaaS, PaaS, and SaaS. Let’s recap these three models. I indicates infrastructure, P indicates platform, and S indicates software. They represent different levels of service. From IaaS to SaaS, making it more convenient for users to use, meanwhile customization and lower-layer resource control are reduced. You can select services at different levels based on your requirements. In the next section, we will learn the architecture of cloud computing.

---

### Modul: Terminology

Term

Full name

Description

IaaS

Infrastructure as a Service

Infrastructure as a service (IaaS) enables consumers to use processing, storage, network, and various basic computing resources to deploy and execute various software such as operating systems or applications without purchasing hardware devices such as servers and networks. Customers cannot manage or control underlying infrastructure. However, they can control operating systems, storage devices, and deployed applications. Sometimes, they can control specific network elements, such as the host firewall, to a certain extent.

PaaS

Platform as a Service

PaaS is an application hosting and running environment. It is an efficient development platform (development tools and a large number of middleware services) and provides DevOps/NoOps capabilities (O&M automation or O&M outsourcing).

SaaS

Software as a Service

In this model, cloud providers install and operate application software in the cloud and cloud users access the software from cloud clients. The cloud users do not manage the cloud infrastructure and platform on which the application is running. This eliminates the need to install and run the application on the cloud user's own computers simplifying maintenance and support.

ECS

Elastic Cloud Server

An Elastic Cloud Server (ECS) is a computing server that consists of CPUs, memory, images, and Elastic Volume Service (EVS) disks and allows on-demand allocation and elastic scaling.

EVS

Elastic Volume Service

Elastic Volume Service (EVS) disks are a type of virtual block storage devices that use the distributed architecture and can be elastically expanded.

VFW

Virtual Firewall

A network firewall service or appliance running in a virtualized environment to provide the usual packet filtering and monitoring functions like a physical network firewall.

CRM

Customer Relationship Management

An enterprise business strategy, which is used to organize enterprise resources effectively, cultivate customer-centric operational behaviors and implement customer-centric business processes, so as to raise profitability, revenue and customer satisfaction.

---

### Modul: Quiz

随堂测验

10 /10

Unlimited

--

---

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

---

# Chapter 08: Cloud: Enabler of New Techs

- **Deskripsi:** Cloud Sebagai Fondasi Teknologi Baru (AI, Big Data, IoT, 5G)
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Cloud: Enabler of New Techs

Cloud: Enabler of New Techs

In the last section, we learned about cloud computing architecture. In this section, we will focus on how cloud computing supports other key technologies that change the world. The future will be a fully connected, intelligent society, which relies on a variety of technologies, such as AI, IoT, 5G, Cloud Computing and so on. What role does cloud computing play in it? Cloud computing features powerful and scalable computing capabilities with effective and flexible investment making it an important supporter and enabler of other technologies. Let's use an analogy to illustrate their relationships. If an intelligent world is a computer, cloud computing will be its CPU and hard disks, and provides computing and storage capabilities. While IoT devices are input and output devices like mouse, keyboard, and monitor, for data collection and output. AI is an application program, which defines data usage and focuses on data analysis and application. Last one is 5G, it functions as an ultra-high-speed network cable that can connect massive keyboards, mouses and monitors around the world with the computer. Now let's briefly introduce these concepts. First, IoT, The Internet of things. The concept of IoT is derived from the Internet. It is the "Internet for things", which is a network of physical objects. We use RFID, sensors, embedded systems to track and collect information. For example, the temperature of your house, the road conditions around an autonomous driving car. The data can be transferred to the cloud, and the cloud IoT platform can assist in data storage and analysis. Many public cloud vendors provide IoT support, such as the IoT Device Management service on HUAWEI CLOUD. IoT can be applied to many fields, such as smart home, industry, agriculture, transportation, smart grid and environmental protection. Then, Artificial intelligence. Artificial intelligence is a topic everyone is talking about. A few years ago, AlphaGo, the AI robot developed by Google, winning the World Go Championship, sparked the world's attention to AI. The elements of AI include the following four:Big data, Computing capability, Algorithm, and scenario. Applications of AI including robotics, speech recognition, image recognition, and natural language processing. All of them require powerful computing capabilities. Artificial intelligence is located at the application layer and transforms computing power in cloud into scenario-based applications. Another area closely related to cloud computing is 5G. The advantages of 5G Network are large bandwidth, low latency, and massive connection. 5G brings faster data transmission speeds and data throughput, making cloud computers and cloud games perform better. It can support remote real-time medical surgery and better applications of latency-sensitive things such as VR, AR. Wide connectivity of 5G allows more IoT devices to connect to the Internet and communicate with cloud. Also, cloud computing benefits the development of 5G. 5G can use cloud computing to virtualize some access and core network devices, then software and hardware decoupled, which improves network efficiency. In addition, the edge cloud effectively reduces 5G transmission latency. In the future, IoT, cloud computing, artificial intelligence, 5G and other technologies will increasingly be integrated and applied to industry upgrades and community intelligence. Among them, cloud computing will be an important digital infrastructure for society. It is an irreplaceable part of enabling other enterprise applications and intelligent scenarios. In this class, we have learned some technologies driving the world more digital and intelligent together with cloud. And cloud computing plays an essential role in the development of other technologies. Next, we will talk about some trends of cloud computing.

---

### Modul: Terminology

Term

Full name

Description

IoT

Internet of Things

The Internet of things is the network of physical devices, vehicles, home appliances and other items embedded with electronics, software, sensors, actuators, and network connectivity which enables these objects to connect and exchange data.

RFID

Radio  Frequency Identification

Radio-frequency identification (RFID) is the wireless non-contact use of radio-frequency electromagnetic fields to transfer data, for the purposes of automatically identifying and tracking tags attached to objects. It uses radio frequencies to identify objects and obtain data without manual intervention.

NFV

Network Functions Virtualization

Network Functions Virtualization (NFV) uses IT virtualization technologies to consolidate many network equipment types onto industrial standards, such as servers, switches, and storage, which could be located in data centers, network nodes, and in end user premises.

---

### Modul: Quiz

随堂测验

10 /10

Unlimited

--

---

# Chapter 09: Cloud Trends

- **Deskripsi:** Tren Cloud Masa Depan: Cloud-Native, Serverless, Edge Computing
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Cloud Trends

Cloud Trends

In the last class, We have learned some technologies driving the world to become more digital and intelligent together with cloud. And cloud computing plays an important role in the development of other technologies. Today, we will discuss the development trend of cloud computing. Cloud is an evolving concept. What will the cloud look like in the future? Search for cloud trends we can find many answers, such as Serverless、Edge Computing、Multi-cloud、Cloud Game、Mobile Office. Here we focus on two most important technologies. One is cloud native and the other is cloud-edge collaboration. First, what is cloud native? According to the definition from the CNCF: Cloud native technologies empower organizations to build and run scalable applications in modern, dynamic environments such as public, private, and hybrid clouds. Containers, service meshes, microservices, immutable infrastructure, and declarative APIs exemplify this approach. Generally, cloud native includes technologies (microservices and containers) and organization and management (DevOps, CI/CD), which is a collection of cloud technologies and enterprise management methods. Instead of focusing on migrating applications to cloud, cloud-native features constructing and providing applications based on cloud characteristics. Among these technologies and methods, the most popular one is the container technology. What is container? It is a popular application packaging solution. Application and the required environment are packaged into images for development, shipment and deployment. An image is a read-only template used to create container instances. One mainstream container product is Docker. The containers are lightweight and portable. Compared with a virtual machine, it is more lightweight and consumes less resources. So that thousands of containers can run concurrently on a server. Containers feature portability as well. Because a container encapsulates an application and all its dependencies, the application can easily run on different platforms, either traditional servers or clouds. Using image repository, images can be shared and distributed conveniently. This is container, an important part of cloud-native. The second trend of cloud is cloud-edge collaboration. For Cloud computing, data is transmitted to data centers, and in remote data centers, compute tasks are completed. However, in the era of 5G and Internet of Things, more and more terminals are participating and more data are being generated. The traditional cloud mode has faced many bottlenecks, such as insufficient bandwidth, high power consumption, and insufficient real-time performance. Edge computing places the computing process close to the source end of data generation, which is the origin of “edge”.Edge devices can be mobile phones, laptops, industrial robots, and so on. In this way, the data is processed in real-time, ensuring low-latency performance, saving network bandwidth, and reducing the pressure on the data center. A typical application is autonomous driving. For autonomous driving cars, even a delay of a few milliseconds can lead to accidents and catastrophic losses. Autonomous cars must respond immediately to the changing road conditions and cannot simply stop while waiting for instructions or advice from remote cloud server’s analysis data. If the sensor data is analyzed near the local edge device, the network latency problem can be solved well. Edge computing cannot replace cloud computing. The powerful computing capability and resource scalability of cloud computing are irreplaceable. In the future, cloud and edge will be better coordinated to implement various intelligent applications.To sum up, cloud native focuses on application development and management. It is a collection of technologies and methods, making application delivery more agile and efficient and enabling enterprises to respond to services more quickly. Cloud-edge collaboration is another direction of cloud computing development. This concept is more macroscopic. Edge computing is an extension of cloud computing which can meet the requirements of low latency. Cloud computing is still developing rapidly. Cloud Native and Edge Computing are only two of these trends. In the future, cloud computing will become the foundation of information technology. Thank you for participating in this course. If you are interested, you can continue to learn and explore more about cloud computing. Based on the importance of cloud computing in today's IT society, having the knowledge and understanding of cloud computing can help you develop faster and better.

---

### Modul: Terminology

Term

Full name

Description

edge computing

/

Edge computing is pushing the frontier of computing applications, data, and services away from centralized nodes to the logical extremes of a network. It enables analytics and knowledge generation to occur at the source of the data.

---

### Modul: Quiz

随堂测验

5 /5

Unlimited

--

---

# Chapter 10: Master Terminology & Course Summary

- **Deskripsi:** Rangkuman Seluruh Glosarium Terminologi Resmi Huawei & Rangkuman Materi
- **Program:** Seeds for the Future / Huawei Talent Official Course
- **Kursus:** Development and Basic Concepts of Cloud Computing

---

## Isi Materi & Narasi Pembelajaran

### Modul: Summary

Terminology Summary

Summary

Outline

Terminology in Cloud Basic Course

Term

Full name

Description

OBS

Object Storage Service

An object-based cloud storage service. It provides data storage of easy extensibility, high security, proven reliability, and high cost efficiency.

EIP

Elastic IP Address

The Elastic IP Address (EIP) service provides independent public IP addresses and bandwidth to the Internet. An EIP can be flexibly associated with or disassociated from an ECS, BMS, virtual IP address, load balancer, or NAT gateway. Various billing modes are provided to meet diversified service requirements.

Term

Full name

Description

ARM

Advanced Reduced Instruction Set Computing Machines

Reduced instruction set computing, is a CPU design strategy based on the insight that a simplified instruction set provides higher performance when combined with a microprocessor architecture capable of executing those instructions using fewer microprocessor cycles per instruction. A computer based on this strategy is a reduced instruction set computer.

VMware

/

A leader in virtualization technology. VMware provides a portfolio of software products for virtualizing hardware resources to enable one physical server to take the role of multiple servers.

X86

/

x86 is the generic name for Intel processors released after the original 8086 processor.

OpenStack

/

OpenStack is a free and open-source software platform for cloud computing, mostly deployed as Infrastructure as a Service (IaaS), whereby virtual servers and other resources are made available to customers. The software platform consists of interrelated components that control diverse, multi-vendor hardware pools of processing, storage, and networking resources throughout a data center.

Docker

/

The term docker can refer to The Docker project as a whole, which is a platform for developers and sysadmins to develop, ship, and run applications the docker daemon process running on the host which manages images and containers

VPN

Virtual Private Network

The term describes any technology that can encapsulate and transmit network data, typically Internet Protocol data, over another network. Such a system enables users to access network resources that may otherwise be inaccessible from the public internet.

DNS

·        Domain Name Server

A functional entity in the TCP/IP network. With deployment of the DNS, subscribers can access related servers using corresponding domain names. In the TCP/IP network, a domain name maps an IP address. Domain names are easier to remember but servers in the network communicate with each other using IP addresses. Therefore the DNS is used to convert domain names to corresponding IP addresses.

TCP/IP

Transmission Control Protocol/Internet Protocol

Common name for the suite of protocols developed to support the construction of worldwide internetworks.

WWW

·        World Wide Web

A large scale hypermedia information system that allows users to browse information.

ESXi

/

A virtualization platform for creating and running virtual machines. ESXi virtualizes processor, memory, and storage resources and allocates the resources for virtual machines. Virtual machines, operating systems, and applications can run above the ESXi.

Xen

Xen is a Hypervisor providing services that allow multiple computer operating systems to execute on the same computer hardware concurrently.

KVM

·        Kernel-based Virtual Machine

Kernel-based Virtual Machine (KVM) is a virtualization infrastructure for the Linux kernel. KVM requires a processor with hardware virtualization extension.

LXC

Linux Container

LXC (Linux Containers) is an operating-system-level virtualization method for running multiple isolated Linux systems (containers) on a control host using a single Linux kernel.

Hyper-V

/

A VM system provided by Microsoft, which is installed on hosts.

EC2

Elastic Compute Cloud

Amazon Elastic Computing Cloud (Amazon EC2) is a web service provided by Amazon. It enables users to rent cloud computers to run required applications.

S3

Simple Storage Service

Amazon Simple Storage Service is storage for the Internet. It is designed to make web-scale computing easier for developers.

Term

Full name

Description

CAPEX

Capital Expenditure

Capital expenditures (CAPEX or capex) are expenditures creating future benefits. A capital expenditure is incurred when a business spends money either to buy fixed assets or to add to the value of an existing fixed asset with a useful life that extends beyond the taxable year.

OPEX

Operating Expense

An operating expense, operating expenditure, operational expense, operational expenditure or OPEX is an ongoing cost for running a product, business, or system.

TCO

Total Cost of Ownership

Total cost of ownership (TCO) is a financial estimate whose purpose is to help consumers and enterprise managers determine direct and indirect costs of a product or system. It is a management accounting concept that can be used in full cost accounting or even ecological economics where it includes social costs.

Term

Full name

Description

IaaS

Infrastructure as a Service

Infrastructure as a service (IaaS) enables consumers to use processing, storage, network, and various basic computing resources to deploy and execute various software such as operating systems or applications without purchasing hardware devices such as servers and networks. Customers cannot manage or control underlying infrastructure. However, they can control operating systems, storage devices, and deployed applications. Sometimes, they can control specific network elements, such as the host firewall, to a certain extent.

PaaS

Platform as a Service

PaaS is an application hosting and running environment. It is an efficient development platform (development tools and a large number of middleware services) and provides DevOps/NoOps capabilities (O&M automation or O&M outsourcing).

SaaS

Software as a Service

In this model, cloud providers install and operate application software in the cloud and cloud users access the software from cloud clients. The cloud users do not manage the cloud infrastructure and platform on which the application is running. This eliminates the need to install and run the application on the cloud user's own computers simplifying maintenance and support.

ECS

Elastic Cloud Server

An Elastic Cloud Server (ECS) is a computing server that consists of CPUs, memory, images, and Elastic Volume Service (EVS) disks and allows on-demand allocation and elastic scaling.

EVS

Elastic Volume Service

Elastic Volume Service (EVS) disks are a type of virtual block storage devices that use the distributed architecture and can be elastically expanded.

VFW

Virtual Firewall

A network firewall service or appliance running in a virtualized environment to provide the usual packet filtering and monitoring functions like a physical network firewall.

CRM

Customer Relationship Management

An enterprise business strategy, which is used to organize enterprise resources effectively, cultivate customer-centric operational behaviors and implement customer-centric business processes, so as to raise profitability, revenue and customer satisfaction.

Term

Full name

Description

IoT

Internet of Things

The Internet of things is the network of physical devices, vehicles, home appliances and other items embedded with electronics, software, sensors, actuators, and network connectivity which enables these objects to connect and exchange data.

RFID

Radio  Frequency Identification

Radio-frequency identification (RFID) is the wireless non-contact use of radio-frequency electromagnetic fields to transfer data, for the purposes of automatically identifying and tracking tags attached to objects. It uses radio frequencies to identify objects and obtain data without manual intervention.

NFV

Network Functions Virtualization

Network Functions Virtualization (NFV) uses IT virtualization technologies to consolidate many network equipment types onto industrial standards, such as servers, switches, and storage, which could be located in data centers, network nodes, and in end user premises.

Term

Full name

Description

edge computing

/

Edge computing is pushing the frontier of computing applications, data, and services away from centralized nodes to the logical extremes of a network. It enables analytics and knowledge generation to occur at the source of the data.

---

### Modul: Outline

Terminology Summary

Outline

Outline