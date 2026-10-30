# Chapter 06: OpenStack, Cloud Services, and Maintenance Tools (OpenStack, Layanan Cloud, & Perangkat O&M)

- **Kursus:** General Knowledge of Cloud Computing (Huawei Official Course)
- **Modul Video:** `6. OpenStack, Cloud Services, and Maintenance Tools`
- **Presenter:** Zack (Huawei Technologies)

---

## 1. Narasi Transkrip Video Resmi (English Transcript)

And this chapter will learn about openstart.The leading cloud operating system will also discuss basic cloud services like a lastic cloud server and object storage service.

Finally,it will see how these major parts the cloud interact with the tools used by cloud administrators.

Here's an overall view of this lesson on the bottom left side are the parts of the cloud discucusred earlier cloudds physical harbard infrastructure.The virtual machine in the hypervisor above that is the cloud os openstack.

And its components will take a look at these in detail in a moment and on the top of our cloud services,what the cloud provides to users will also look at this anmmor,too.Now on the right,you can see the column cold tools as you can see.

Cloud can be supercomplicated.So poools are what cloud ammans need to operate the cloud more smoothlely.These tools are similar to what you see on your own pc theylike,the diagnostis and other utilities that help you identify harbor problems or check if your drivers are up today.

In cloud tools are used to identify faulty harddrives to backup rogs upgrade systems,support harbor replacement,ment,perform other other mine tasks out the beginning of his lesson imengine two services.

As a cloud users,services are the things you actually pay for.Let me give you a few examples.Alastic cloud server or ecs is about rapidly scaling up your computing resources according to you or your organiza's needs as we saw earlier.

Elasastic scaling is what companies used to deal with service peaks,like there's a big onmind cell.There's a service called autoscaling,which is similar,but the processes more automated compared to ecs,there's also vpc or virtual private cloud.

It's a service used for network isolation,basically using a virtual private network to access cloud services.As you consee there,many,many,many services on the cloud.This is probably why people get paid so much to manage clouds,it's complicated.

Now it's time to talk more about openstack.Among all the layers here is probably the one that's newest to you as binched.It's the most popular operating system for clouds like linux,android and many other major software platforms,openstack is open source.

Opensource software refers to software that is developed collaboratily,if if people all around a rote,so it developers conceal the source code and contribute their own.This is typically done,undedicated,sharing plathorers.

Wanch in two thousand and ten openstack is managed by the open infrastructure foundation over five hundred companies.Roadwiright contribute to openstacks mainments and upgraits.In many ways,openstack operates like an online store.

It manages product,such as computing,storage and network resources that are sold for you some the cloud a product that it cells are allocated by hiyvisors like kvm that we discussed in the previous chapter.It open speacks a service at the IS layer.

And it is used to manage infrastructure.It simplifizes the cloud flute process and provides good scale ability opens that consists of multiple key components that communicate their message cues.

These components work together to implement all kinds of operations that make use of openstacks kit filties over time,contributors about a more and more components to improve opensex functionality.The core component of openstack is the computing component nova.

Which is used to viralize resources.Ces create various virtual machines.Nobody is the openstack component that oversees cpu and memory resources and allocaaces resources to vamps.

If no vsounound similar to cavm,when we talked about in the previous chapter,that's because it is they do the same thing,but at different layers in the cloud,this is the layer that cloud admins.See,where's everything else happens behind the scenes at lower layers?

Some people see nova as a cavm interface that manages vm life cycles,unlike cavm nova focuses on scheduling,while handling computer requests reusers nova communicates with other cloud components and slets,which host hypervisor to use.

But in fact,nobody doesn't actually do the machine virtualialization itself,then we up components that manage storage,openstack block storage component is called cinder.

It's designed to create and manage a service that provides persistent data storage for cloud computing applications.Sender manages where data stored,whether that's on a local desor on a remote location somewhere.I'm a cloud network,then we have open stx network compone called neutron.

Neutron provides the virtunetwork function in the taud competing environment.It hopes flexibly divide physical networks and provides an independent network environment for each time and a multititive.This environ,the last component all mention is the authentication component.

Keystone keystone is like a doormanor manager that has the keyed to all of openstack services kestone not only identifies who you are as the user,but also what you can do.These are two different things.

First,he's don't checks,whether you can log into the system at all.Secondly,it checks whether youd have the permission to process certain requests.I know that was a lot.So let's stop right there.And the next lesson will talk about where cloud is heading in the future.

---

## 2. Transkrip Detail Timeline (Timestamp)

- **`[00:00:14.124 - 00:00:23.124]`** And this chapter will learn about openstart.The leading cloud operating system will also discuss basic cloud services like a lastic cloud server and object storage service.
- **`[00:00:23.840 - 00:00:28.610]`** Finally,it will see how these major parts the cloud interact with the tools used by cloud administrators.
- **`[00:00:29.808 - 00:00:42.968]`** Here's an overall view of this lesson on the bottom left side are the parts of the cloud discucusred earlier cloudds physical harbard infrastructure.The virtual machine in the hypervisor above that is the cloud os openstack.
- **`[00:00:43.036 - 00:00:56.166]`** And its components will take a look at these in detail in a moment and on the top of our cloud services,what the cloud provides to users will also look at this anmmor,too.Now on the right,you can see the column cold tools as you can see.
- **`[00:00:56.484 - 00:01:09.784]`** Cloud can be supercomplicated.So poools are what cloud ammans need to operate the cloud more smoothlely.These tools are similar to what you see on your own pc theylike,the diagnostis and other utilities that help you identify harbor problems or check if your drivers are up today.
- **`[00:01:10.504 - 00:01:21.744]`** In cloud tools are used to identify faulty harddrives to backup rogs upgrade systems,support harbor replacement,ment,perform other other mine tasks out the beginning of his lesson imengine two services.
- **`[00:01:22.092 - 00:01:35.472]`** As a cloud users,services are the things you actually pay for.Let me give you a few examples.Alastic cloud server or ecs is about rapidly scaling up your computing resources according to you or your organiza's needs as we saw earlier.
- **`[00:01:35.816 - 00:01:49.256]`** Elasastic scaling is what companies used to deal with service peaks,like there's a big onmind cell.There's a service called autoscaling,which is similar,but the processes more automated compared to ecs,there's also vpc or virtual private cloud.
- **`[00:01:49.576 - 00:02:02.686]`** It's a service used for network isolation,basically using a virtual private network to access cloud services.As you consee there,many,many,many services on the cloud.This is probably why people get paid so much to manage clouds,it's complicated.
- **`[00:02:03.524 - 00:02:17.494]`** Now it's time to talk more about openstack.Among all the layers here is probably the one that's newest to you as binched.It's the most popular operating system for clouds like linux,android and many other major software platforms,openstack is open source.
- **`[00:02:18.100 - 00:02:28.500]`** Opensource software refers to software that is developed collaboratily,if if people all around a rote,so it developers conceal the source code and contribute their own.This is typically done,undedicated,sharing plathorers.
- **`[00:02:29.188 - 00:02:41.588]`** Wanch in two thousand and ten openstack is managed by the open infrastructure foundation over five hundred companies.Roadwiright contribute to openstacks mainments and upgraits.In many ways,openstack operates like an online store.
- **`[00:02:41.948 - 00:02:55.908]`** It manages product,such as computing,storage and network resources that are sold for you some the cloud a product that it cells are allocated by hiyvisors like kvm that we discussed in the previous chapter.It open speacks a service at the IS layer.
- **`[00:02:56.152 - 00:03:06.622]`** And it is used to manage infrastructure.It simplifizes the cloud flute process and provides good scale ability opens that consists of multiple key components that communicate their message cues.
- **`[00:03:06.992 - 00:03:20.962]`** These components work together to implement all kinds of operations that make use of openstacks kit filties over time,contributors about a more and more components to improve opensex functionality.The core component of openstack is the computing component nova.
- **`[00:03:21.224 - 00:03:31.204]`** Which is used to viralize resources.Ces create various virtual machines.Nobody is the openstack component that oversees cpu and memory resources and allocaaces resources to vamps.
- **`[00:03:31.560 - 00:03:43.800]`** If no vsounound similar to cavm,when we talked about in the previous chapter,that's because it is they do the same thing,but at different layers in the cloud,this is the layer that cloud admins.See,where's everything else happens behind the scenes at lower layers?
- **`[00:03:44.512 - 00:03:58.412]`** Some people see nova as a cavm interface that manages vm life cycles,unlike cavm nova focuses on scheduling,while handling computer requests reusers nova communicates with other cloud components and slets,which host hypervisor to use.
- **`[00:03:58.928 - 00:04:07.698]`** But in fact,nobody doesn't actually do the machine virtualialization itself,then we up components that manage storage,openstack block storage component is called cinder.
- **`[00:04:08.336 - 00:04:22.146]`** It's designed to create and manage a service that provides persistent data storage for cloud computing applications.Sender manages where data stored,whether that's on a local desor on a remote location somewhere.I'm a cloud network,then we have open stx network compone called neutron.
- **`[00:04:22.388 - 00:04:36.118]`** Neutron provides the virtunetwork function in the taud competing environment.It hopes flexibly divide physical networks and provides an independent network environment for each time and a multititive.This environ,the last component all mention is the authentication component.
- **`[00:04:36.252 - 00:04:47.372]`** Keystone keystone is like a doormanor manager that has the keyed to all of openstack services kestone not only identifies who you are as the user,but also what you can do.These are two different things.
- **`[00:04:47.768 - 00:05:00.778]`** First,he's don't checks,whether you can log into the system at all.Secondly,it checks whether youd have the permission to process certain requests.I know that was a lot.So let's stop right there.And the next lesson will talk about where cloud is heading in the future.

---

## 3. Rangkuman Poin Kunci & Intisari Ujian (Key Exam Takeaways)

- **OpenStack sebagai Cloud Operating System:**
  - Platform open-source untuk mengendalikan kolam besar komputasi, penyimpanan, dan jaringan di data center.
  - **Modul Inti:**
    - *Nova:* Manajemen siklus hidup komputasi virtual.
    - *Neutron:* Software-Defined Networking (SDN) dan IP management.
    - *Cinder:* Block storage service.
    - *Glance:* Image repository OS.
    - *Keystone:* Autentikasi identitas dan otorisasi token.
    - *Horizon:* Dashboard web GUI manajemen.
- **Perangkat Operasi & Pemeliharaan (O&M):**
  - Alarm monitoring, log auditing, capacity planning, dan automasi deployment.