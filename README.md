```
# VXLAN-Simulation
> VXLAN-Simulation is a project designed to demonstrate the encapsulation of Layer 2 packets in an IP/UDP network using VXLAN.
> The system allows for the simulation of a flexible virtual network topology, ensuring proper data transmission between hosts via VXLAN tunnels.
> VXLAN packets are analyzed with **Wireshark** to verify the encapsulation and transport of data between virtualized hosts.
## 📌 Contents
- [Project Structure](#project-structure)
- [What is VXLAN](#what-is-vxlan)
- [Topology Description](#topology-description)
- [Workflow Description](#workflow-description)
- [Multimedia Material](#multimedia-material)
- [Contributors](#contributors)

## 📁 Project Structure
The project structure is organized as follows:
```
VXLAN-Simulation/
│── src/                     # Main source code
│   ├── vxlan_topology_1.py  # First Mininet Topology with VXLAN configuration
│   ├── vxlan_topology_2.py  # Second Mininet Topology and VXLAN configuration
│── captures/                # Images and files documenting packet capture
│   ├── cattura_gener.png    # Image 1
│   ├── vxlan_head.png       # Image 2
│   ├── vxlan_packs.png      # Image 3
│── docs/                    # Project documentation
│── README.md                # Main documentation
```
---
## 🌐 What is VXLAN
VXLAN (**Virtual eXtensible Local Area Network**) is a **tunneling** protocol that extends Layer 2 networks over a **Layer 3** infrastructure using **UDP/IP**. Designed to overcome the limitations of traditional VLANs, VXLAN offers greater scalability and flexibility.
### **Key Features**
| Feature                   | VLAN               | VXLAN                                   |
| -------------------------- | ------------------ | --------------------------------------- |
| **Network Identifier**     | VLAN ID (12 bit)   | VXLAN Network Identifier (VNI - 24 bit) |
| **Maximum Number of Networks** | 4096 VLAN          | ~16 million VXLAN                       |
| **Scope**                  | Layer 2 (Ethernet) | Layer 3 (IP/UDP)                        |
| **Tunneling**              | No                 | Yes (UDP 4789)                          |
| **Scalability**            | Limited            | High                                    |
- VXLAN uses a **VNI (VXLAN Network Identifier) of 24 bits**, allowing up to **16 million virtual networks**.
- Ethernet frames are encapsulated in **UDP packets**, making VXLAN compatible with existing IP infrastructure.
### **Key Components of VXLAN**
- **VTEP (VXLAN Tunnel EndPoint)**: devices that encapsulate and de-encapsulate VXLAN traffic.
- **Outer IP Header**: the outer packet that carries VXLAN traffic over UDP.
- **UDP Header (port 4789)**: UDP transport enables VXLAN communication over Layer 3 networks.
- **VXLAN Header**: contains the **VNI**, which identifies the virtual network.
- **Inner Ethernet Frame**: the original Ethernet packet encapsulated within the tunnel.
### **VXLAN Packet Structure**
| **Layer** | **Component** | **Description** |
|------------|--------------|----------------|
| 1 | **Ethernet (Outer Ethernet Frame)** | Outer Ethernet frame for VXLAN encapsulation |
| 2 | **IP Header (Outer IP Header)** | Outer IP header for VXLAN tunneling |
| 3 | **UDP Header (Dest. Port 4789 - VXLAN)** | UDP header with destination port 4789 (standard VXLAN) |
| 4 | **VXLAN Header** | VXLAN header containing virtualization information |
| 4.1 | **Flag** | Control bits to identify the VXLAN packet |
| 4.2 | **VXLAN Network Identifier (VNI)** | VXLAN network identifier (24 bits) |
| 5 | **Ethernet (Inner Ethernet Frame)** | Original Ethernet frame transported inside the tunnel |
| 6 | **Original Payload** | Original data (IP, ARP, ICMP, etc.) encapsulated in the VXLAN tunnel |
### **Advantages of VXLAN**
- ✔ **Scalability**: up to 16 million virtual networks.
- ✔ **Layer 3 Support**: tunneling over UDP to extend connectivity between data centers.
- ✔ **Traffic Isolation**: better network separation compared to VLANs.
- ✔ **SDN Integration**: VXLAN is compatible with network controllers for dynamic management.
### **How VXLAN Tunneling Works**
1. A host sends an **Ethernet packet** to a VTEP.
2. The VTEP **encapsulates** the Ethernet packet into a **VXLAN packet** with the appropriate **VNI**.
3. The VXLAN packet is forwarded over the **IP network** as a normal UDP packet.
4. The destination VTEP **de-encapsulates** the packet, restoring the original Ethernet frame.
5. The Ethernet frame is sent to the final destination.

## 🗺️ Topology Description
For this project, I simulated two different topologies, one with the file **vxlan_topology_1.py** and another with the file **vxlan_topology_2.py**.
### 1️⃣ Topology from the file **vxlan_topology_1.py**:
The topology simulated in the project consists of:
- **Two OVS switches** connected via a VXLAN tunnel.
- **Three hosts**, **h1** connected to switch **s1**, while **h2** and **h3** are connected to switch **s2**.
- Host **h1** communicates with hosts **h2** and **h3** using the **VXLAN tunnel**, while **h2** and **h3** communicate with each other via **VLAN**, since they belong to the same switch.
The topology diagram is as follows:
```
[ h1 ] --- (s1) --- VXLAN Tunnel --- (s2) --- [ h2 ]
                                      |
                                      |
                                    [ h3 ]
```
### 2️⃣ Topology from the file **vxlan_topology_2.py**:
The topology simulated in the project consists of:
- **Two OVS switches** connected via a VXLAN tunnel.
- **Two hosts**, h1 and h2 connected respectively to the two switches.
The topology diagram is as follows:
```
[ h1 ] --- (s1) --- VXLAN Tunnel --- (s2) --- [ h2 ]
```
Each Open vSwitch (OVS) is configured to encapsulate traffic coming from the host into a VXLAN packet and send it through the tunnel.

## 🚀 Installation & Running the Project
### **Guide to Installing and Configuring the Virtual Machine on VirtualBox**
1. **Install VirtualBox** by downloading it from the official website:  
   🔗 [VirtualBox Download](https://www.virtualbox.org/wiki/Downloads).  
2. **Download the virtual machine** from the following link:  
   🔗 [Download VM Image](https://drive.google.com/drive/folders/1FP5Bx2DHp7oV57Ja38_x01ABiw3wK11M?usp=sharing).
3. **Import the virtual machine** into VirtualBox:  
   - Open **VirtualBox** and go to **File → Import Appliance**.  
   - Select the downloaded **.ova** file and follow the instructions for importation.
4. **Configure the virtual machine** after importing:  
   - Go to **Settings → System → Processor** and assign an adequate number of CPUs.  
   - Go to **Settings → System → Memory** and assign a sufficient amount of RAM.  
5. **Start the virtual machine** via VirtualBox.
6. **Connect to the VM via SSH** for easier management:  
   - Open a terminal on your computer and use the command:  
     ```
     ssh -X -p 2222 vagrant@localhost
     ```
   - When prompted, enter the password: **vagrant**.
7. **Install MobaXterm** if you want to run Wireshark on the VM with graphical support:  
   - Download and install **MobaXterm** from the official site:  
     🔗 [MobaXterm Download](https://mobaxterm.mobatek.net/download.html).  
   - Open **MobaXterm** and connect to the VM using the same SSH command:  
     ```bash
     ssh -X -p 2222 vagrant@localhost
     ```
8. **Create a folder in the VM and transfer files with SCP**:  
   - Access the virtual machine via SSH and create the folder where the file will be saved:
     ```
     mkdir -p /home/vagrant/vxlan_project
     ```
   - From your local computer, use the **scp** command to transfer the file:  
     ```
     scp -P 2222 C:\Path\To\File\To\Transfer\file.py vagrant@localhost:/home/vagrant/vxlan_project
     ```
   - The file will now be available in the `/home/vagrant/vxlan_project` folder on the virtual machine.

## 🔄 Workflow Description
To test the VXLAN simulation, follow these steps:
1️⃣ **Start the VXLAN network topology**  
   - Run the script to create the virtual network with Mininet and configure the VXLAN tunnels:
   ```
   sudo python3 vxlan_topology_1.py
   ```
2️⃣ **Connect to the virtual machine with MobaXterm to run Wireshark with a graphical interface**  
   - Open **MobaXterm** and connect to the VM where the simulation is running and run Wireshark:
   ```
   sudo wireshark
   ```
3️⃣ **Capture VXLAN traffic**  
   - Select the **any** interface and apply the filter to intercept VXLAN packets:
   ```
   udp.port == 4789
   ```
4️⃣ **Generate traffic on the simulated network**  
   - On the Mininet terminal, with the VXLAN topology active, run the command to check connectivity between hosts:
   ```
   h1 ping h2
   ```
5️⃣ **Analyze captured packets in Wireshark**  
   - Analyze the captured packets in the application with the "udp.port == 4789" filter active:
<p align="center">
    <img src="captures/vxlan_packet_details.png" width="500">
    <img src="captures/vxlan_header_analysis.png" width="500">
    <img src="captures/cattura_generale.png" width="900">
</p>
  
## 📂 Materials
Below are links to useful materials for the project:
- 🔗 [Video demonstration of execution:](https://www.youtube.com/watch?v=FdMMLcU9ET4&ab_channel=kostazefkilis).
- 🔗 [PDF Presentation of the project:](link_del_pdf.com).
## 👥 Contributors
- **Zefkilis2002**, k.zefkilis@studenti.unitn.it, 226600
- **LucaPio02**, lucapio.pierno@studenti.unint.it, 228904
If you wish to contribute, you can open a pull request or contact me directly! 🚀
```