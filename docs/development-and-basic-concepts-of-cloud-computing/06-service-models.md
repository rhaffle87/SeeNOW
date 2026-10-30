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