# Chapter 05: Cloud Architecture and Key Components (Arsitektur Cloud & Komponen Inti)

- **Kursus:** General Knowledge of Cloud Computing (Huawei Official Course)
- **Modul Video:** `5. Cloud Architecture`
- **Presenter:** Zack (Huawei Technologies)

---

## 1. Narasi Transkrip Video Resmi (English Transcript)

Okay,moving red along in the previous chapter.We look at the difference between private public and hybrid clouds.Now let's take a look at what they have in calm their architecture specifically.

How data service are built to serve balands or even millions of users.At the same time.Now,cloud architetecture can be presented in a lot of different ways,but today,i'm going to stick with a more basic scription.

We can think of cloud architecture as a building.That's three stories tall.The bottom floor is the hardware layer above that is the virtual machine layer.And on top.We have was called the scheduling layer,the building's foundation,the hardware layer.

Also known as the infraccture layer.That's basically the data servers and the networks that connect this equipment can be located very close to the user.In the case of private clouds,the server and networks are often located on site in a server room or even in the basement.

Alternatively,the service can also be located very far away in cooler parts of the world or next to wind parms.I'll talk about wine in a mom.

Cloud servers are very widely sighed from just a few raced.Many,many irax spread across multiple locations.The world's largest stata centers tend to be in places with relatively low average temperatures servverin network equipment produce a lot a heat.

So putting them in more mild climates costless to keep everything cool.This is called heat ticipation and its superimportant in computer.Massive datasenners also tend to be located in places with abfundant renewable energy resources like hydro solar wind power.

Again,this is a cost issue,huge data siitors draw.A lot of power and renewable energy is both cheaper and better for the environment.Next is the virtual machine layer to go back to the building metaphor.This is is second d floor.

Virtual machines are what allow cloud service providers to manage harbard from different locations in a unified way,essentially a virtual machine or vm that you treat different pieces of hardware as one system you could abstract.

Combine and split computing resources anyway that you want this alallows cloud service providers to deliver diversified multay level.And customied cloud computing services to users are on the world.Now virtualization is what makes club computing work.

On the surface,these virtual al machines are independent servers.They don't share data.They may use different operating systems and one beam crashes.If one affect the other ones.

Meanwhile,they also share resources like cpu,memory and network adapters from physical service of physical machine is usually called a host bachy,and a vam is called a gustsheso.So how do virtualize physical resources?

We use a hypervisor sometimes also called a virtual machine monitor.It's a class of software that enabled this kvm,which is a free ernal baselinics tool.

Is by far,the most widely used opensource virtualizzation software in the world,hevium focuses on the virtualization of memory and cpu resources.

Another software tool is needed to virtualize input,put outoutput resources,network cards and disk or fast storage.One of the most popular iodevice virtualalization tools is called cuuimo.In addition.

The virtual machine layer includes another type of virtualization tool to interface with system advins,the most popular ers called lidvert.Strictly speaking,within the virtual machine layer,only cabe of itself is the hypervisor.

But many people often lumpp together,caveum qum,mu,liver and linux and referred it than collectively as the hypervisor,it can give confusing sometimes on the top of this stack.The third layer of the building is the scheduling layer.

The drop of the scheduling layer is to martial cloud resource scheduling identifies a host with spare resources among couands of hosts within a particular cloud.

It's called scheduling because one of its critical roles is to correctly schedule the order in which from various cloud resources are used and tests of perform.You can think of the scheduling layer as the cloud operating system.

Do a laptopsues operating systems,like in s saas.Windows linuics maachaos mobile phones use android harmony os rios to run their apps clouds also have their own operating system.

The most calmly cloudaos is currently openstack.It's become the most popular cloudos because it is open source free.And it's maintained and use together by many smaller large company.So there's a lot of eyes and hands on it.

Openstack can work with a widevariety of software packages and cloud weapons.A cloudos like openstack,it's a critical element and club performance,and the mex lesson will take a closer look at openstack and other cloud management tools.

---

## 2. Transkrip Detail Timeline (Timestamp)

- **`[00:00:07.664 - 00:00:20.054]`** Okay,moving red along in the previous chapter.We look at the difference between private public and hybrid clouds.Now let's take a look at what they have in calm their architecture specifically.
- **`[00:00:20.376 - 00:00:31.066]`** How data service are built to serve balands or even millions of users.At the same time.Now,cloud architetecture can be presented in a lot of different ways,but today,i'm going to stick with a more basic scription.
- **`[00:00:31.584 - 00:00:45.394]`** We can think of cloud architecture as a building.That's three stories tall.The bottom floor is the hardware layer above that is the virtual machine layer.And on top.We have was called the scheduling layer,the building's foundation,the hardware layer.
- **`[00:00:45.584 - 00:00:58.824]`** Also known as the infraccture layer.That's basically the data servers and the networks that connect this equipment can be located very close to the user.In the case of private clouds,the server and networks are often located on site in a server room or even in the basement.
- **`[00:00:59.412 - 00:01:07.042]`** Alternatively,the service can also be located very far away in cooler parts of the world or next to wind parms.I'll talk about wine in a mom.
- **`[00:01:07.888 - 00:01:21.968]`** Cloud servers are very widely sighed from just a few raced.Many,many irax spread across multiple locations.The world's largest stata centers tend to be in places with relatively low average temperatures servverin network equipment produce a lot a heat.
- **`[00:01:22.272 - 00:01:36.232]`** So putting them in more mild climates costless to keep everything cool.This is called heat ticipation and its superimportant in computer.Massive datasenners also tend to be located in places with abfundant renewable energy resources like hydro solar wind power.
- **`[00:01:36.616 - 00:01:49.066]`** Again,this is a cost issue,huge data siitors draw.A lot of power and renewable energy is both cheaper and better for the environment.Next is the virtual machine layer to go back to the building metaphor.This is is second d floor.
- **`[00:01:49.716 - 00:02:02.256]`** Virtual machines are what allow cloud service providers to manage harbard from different locations in a unified way,essentially a virtual machine or vm that you treat different pieces of hardware as one system you could abstract.
- **`[00:02:02.508 - 00:02:15.798]`** Combine and split computing resources anyway that you want this alallows cloud service providers to deliver diversified multay level.And customied cloud computing services to users are on the world.Now virtualization is what makes club computing work.
- **`[00:02:16.120 - 00:02:25.440]`** On the surface,these virtual al machines are independent servers.They don't share data.They may use different operating systems and one beam crashes.If one affect the other ones.
- **`[00:02:25.892 - 00:02:39.512]`** Meanwhile,they also share resources like cpu,memory and network adapters from physical service of physical machine is usually called a host bachy,and a vam is called a gustsheso.So how do virtualize physical resources?
- **`[00:02:40.160 - 00:02:50.370]`** We use a hypervisor sometimes also called a virtual machine monitor.It's a class of software that enabled this kvm,which is a free ernal baselinics tool.
- **`[00:02:50.644 - 00:02:59.154]`** Is by far,the most widely used opensource virtualizzation software in the world,hevium focuses on the virtualization of memory and cpu resources.
- **`[00:02:59.700 - 00:03:11.950]`** Another software tool is needed to virtualize input,put outoutput resources,network cards and disk or fast storage.One of the most popular iodevice virtualalization tools is called cuuimo.In addition.
- **`[00:03:12.280 - 00:03:25.230]`** The virtual machine layer includes another type of virtualization tool to interface with system advins,the most popular ers called lidvert.Strictly speaking,within the virtual machine layer,only cabe of itself is the hypervisor.
- **`[00:03:25.636 - 00:03:39.236]`** But many people often lumpp together,caveum qum,mu,liver and linux and referred it than collectively as the hypervisor,it can give confusing sometimes on the top of this stack.The third layer of the building is the scheduling layer.
- **`[00:03:39.620 - 00:03:49.190]`** The drop of the scheduling layer is to martial cloud resource scheduling identifies a host with spare resources among couands of hosts within a particular cloud.
- **`[00:03:49.584 - 00:04:00.704]`** It's called scheduling because one of its critical roles is to correctly schedule the order in which from various cloud resources are used and tests of perform.You can think of the scheduling layer as the cloud operating system.
- **`[00:04:01.072 - 00:04:12.022]`** Do a laptopsues operating systems,like in s saas.Windows linuics maachaos mobile phones use android harmony os rios to run their apps clouds also have their own operating system.
- **`[00:04:12.482 - 00:04:24.792]`** The most calmly cloudaos is currently openstack.It's become the most popular cloudos because it is open source free.And it's maintained and use together by many smaller large company.So there's a lot of eyes and hands on it.
- **`[00:04:25.272 - 00:04:37.852]`** Openstack can work with a widevariety of software packages and cloud weapons.A cloudos like openstack,it's a critical element and club performance,and the mex lesson will take a closer look at openstack and other cloud management tools.

---

## 3. Rangkuman Poin Kunci & Intisari Ujian (Key Exam Takeaways)

- **Hierarki Arsitektur Cloud Computing:**
  1. **Physical Infrastructure Layer:** Fasilitas data center, server rack/blade, storage array (SAN/NAS), perangkat jaringan switch/router.
  2. **Virtualization Layer (Hypervisor):** Mengubah perangkat keras fisik menjadi kumpulan resource pool logis (vCPU, vRAM, vDisk, virtual switch).
  3. **Cloud Management Layer:** Mengelola orkestrasi, provisioning otomatis, pemantauan kesehatan sistem, High Availability (HA), dan penyeimbangan beban.
  4. **Service & Application Layer:** Antarmuka katalog layanan portal self-service bagi pengguna akhir.