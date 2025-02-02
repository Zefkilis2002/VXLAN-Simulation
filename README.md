# VXLAN-Simulation

> VXLAN-Simulation è un progetto pensato per dimostrare l'incapsulamento di pacchetti Layer 2 in una rete IP/UDP utilizzando VXLAN.
> Il sistema permette di simulare una topologia di rete virtuale flessibile, garantendo la corretta trasmissione dei dati tra host tramite tunnel VXLAN.
> I pacchetti VXLAN vengono analizzati con **Wireshark** per verificare l'incapsulamento e il trasporto dei dati tra host virtualizzati.

## 📌 Contenuti
- [Caratteristiche principali](#caratteristiche-principali)
- [Benefici](#benefici)
- [Dipendenze](#dipendenze)
- [Guida all'installazione](#guida-allinstallazione)
- [Flusso di lavoro](#flusso-di-lavoro)
- [Testing](#testing)

---

## 🛠 Caratteristiche principali

- **Simulazione di una rete VXLAN**:
  - Creazione di una rete virtuale con Mininet.
  - Configurazione di tunnel VXLAN tra due switch OVS.
  - Implementazione di un controller Ryu per la gestione del traffico VXLAN.

- **Analisi del traffico con Wireshark**:
  - Monitoraggio dei pacchetti VXLAN su porta UDP **4789**.
  - Verifica dell'incapsulamento di frame Ethernet Layer 2 in pacchetti IP/UDP.

## 🎯 Benefici

- **Scalabilità**: VXLAN consente di creare reti virtuali su una rete IP esistente, supportando un maggior numero di VLAN.
- **Flessibilità**: Il sistema può essere adattato per gestire più tunnel VXLAN e scenari di rete avanzati.
- **Analisi dettagliata**: Wireshark permette di verificare il corretto funzionamento del protocollo e l'incapsulamento dei pacchetti.

## 🔗 Dipendenze

Per eseguire la simulazione, è necessario installare:

- **Mininet** per la creazione della rete virtuale.
- **Open vSwitch (OVS)** per la configurazione VXLAN.
- **Ryu Controller** per la gestione OpenFlow.
- **Wireshark** per la cattura e analisi dei pacchetti.

Installazione delle dipendenze:
```bash
sudo apt update && sudo apt install mininet openvswitch-switch wireshark python3-ryu
```

## 🚀 Guida all'installazione

1️⃣ **Clonare la repository**:
```bash
git clone https://github.com/Zefkilis2002/VXLAN-Simulation.git
cd VXLAN-Simulation
```

2️⃣ **Avviare la rete VXLAN**:
```bash
sudo python3 src/vxlan_ultimate.py
```

3️⃣ **Avviare il controller Ryu**:
```bash
ryu-manager src/vxlan_controller.py
```

4️⃣ **Verificare la connettività tra gli host**:
```bash
h1 ping h2
```

5️⃣ **Monitorare il traffico VXLAN con Wireshark**:
```bash
tcpdump -i any -nn port 4789
```

---

## 🔄 Flusso di lavoro

1. **Configurazione della topologia Mininet**
    - Due switch OVS collegati tramite un tunnel VXLAN.
    - Due host connessi ai rispettivi switch.

2. **Creazione del tunnel VXLAN**
    - Configurazione automatica tramite Open vSwitch.
    - Flussi OpenFlow aggiunti dal controller Ryu.

3. **Analisi dei pacchetti**
    - Wireshark viene utilizzato per catturare e analizzare i pacchetti VXLAN.
    - Verifica dell'incapsulamento dei frame Layer 2 all'interno dei pacchetti IP/UDP.

## 🔍 Testing

Puoi utilizzare **Wireshark** per analizzare il traffico VXLAN.

Esempio di pacchetto VXLAN catturato:

<p align="center">
    <img src="captures/vxlan_packet_details.png" width="600">
</p>

Analisi dell'intestazione VXLAN:

<p align="center">
    <img src="captures/vxlan_header_analysis.png" width="600">
</p>

---

## 📬 Contatti
Per suggerimenti o miglioramenti, apri una issue su GitHub o contattami direttamente! 🚀

