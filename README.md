# VXLAN-Simulation

> VXLAN-Simulation è un progetto pensato per dimostrare l'incapsulamento di pacchetti Layer 2 in una rete IP/UDP utilizzando VXLAN.
> Il sistema permette di simulare una topologia di rete virtuale flessibile, garantendo la corretta trasmissione dei dati tra host tramite tunnel VXLAN.
> I pacchetti VXLAN vengono analizzati con **Wireshark** per verificare l'incapsulamento e il trasporto dei dati tra host virtualizzati.

## 📌 Contenuti
- [Struttura del progetto](#struttura-del-progetto)
- [Cos'è VXLAN](#cosè-vxlan)
- [Descrizione della topologia](#descrizione-della-topologia)
- [Descrizione WorkFlow](#descrizione-workflow)
- [Materiale multimediale](#materiale-multimediale)
- [Contributors](#contributors)

---

## 📁 Project Structure

La struttura del progetto è organizzata nel seguente modo:
```
VXLAN-Simulation/
│── src/                    # Codice sorgente principale
│   ├── vxlan_controller.py  # Controller Ryu per la gestione del traffico VXLAN
│   ├── vxlan_ultimate.py    # Topologia Mininet e configurazione VXLAN
│── captures/                # Immagini e file che testimoniano la cattura
│   ├── immagine1.png        # Immagine 1
│   ├── immagine2.png        # Immagine 2
│   ├── immagine3.png        # Immagine 3
│── docs/                    # Documentazione del progetto
│── README.md                # Documentazione principale
```

---

## 🌐 Cos'è VXLAN

**VXLAN (Virtual eXtensible LAN)** è un protocollo di incapsulamento che permette di estendere reti Layer 2 attraverso un'infrastruttura Layer 3 utilizzando pacchetti IP/UDP. Questo consente la creazione di reti virtuali scalabili e indipendenti dalla topologia fisica, supportando un maggior numero di segmenti di rete rispetto alle tradizionali VLAN.

Caratteristiche principali di VXLAN:
- Incapsula frame Ethernet all'interno di pacchetti UDP.
- Utilizza il VXLAN Network Identifier (VNI) per separare le reti virtuali.
- Consente la comunicazione tra host su reti diverse senza configurazioni VLAN complesse.
- È utilizzato in ambienti cloud e virtualizzazione di rete.


## 🗺️ Descrizione della Topologia

La topologia simulata nel progetto è composta da:
- **Due switch OVS** connessi tra loro tramite un tunnel VXLAN.
- **Due host** connessi rispettivamente ai due switch.
- **Ryu Controller**, che gestisce le regole di instradamento e l'analisi dei pacchetti.

Il diagramma della topologia è il seguente:

```
[ h1 ] --- (s1) --- VXLAN Tunnel --- (s2) --- [ h2 ]
```

Ogni switch Open vSwitch (OVS) è configurato per incapsulare il traffico proveniente dall'host in un pacchetto VXLAN e inviarlo attraverso il tunnel.

---

## 🚀 Installazione & esecuzione del progetto

### 1️⃣ Installare le dipendenze
Per eseguire il progetto, è necessario installare:
```bash
sudo apt update && sudo apt install mininet openvswitch-switch wireshark python3-ryu
```

### 2️⃣ Clonare la repository
```bash
git clone https://github.com/Zefkilis2002/VXLAN-Simulation.git
cd VXLAN-Simulation
```

### 3️⃣ Avviare la simulazione della rete
```bash
sudo python3 src/vxlan_ultimate.py
```

### 4️⃣ Avviare il controller Ryu
```bash
ryu-manager src/vxlan_controller.py
```

### 5️⃣ Verificare la connettività tra gli host
```bash
h1 ping h2
```

### 6️⃣ Monitorare il traffico VXLAN con Wireshark
```bash
tcpdump -i any -nn port 4789
```

---

## 🔄 Descrizione del WorkFlow

1️⃣ **Configurazione della rete**
   - Mininet avvia due switch OVS e due host.
   - Viene stabilito un tunnel VXLAN tra gli switch.

2️⃣ **Gestione del traffico con Ryu**
   - Il controller riceve pacchetti e applica le regole di instradamento.
   - Registra i pacchetti VXLAN e i loro dettagli (VNI, IP, MAC).

3️⃣ **Cattura e analisi con Wireshark**
   - Wireshark monitora i pacchetti UDP sulla porta 4789.
   - È possibile esaminare l'intestazione VXLAN e il frame Ethernet incapsulato.

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

## 📂 Material

Esempio di pacchetto VXLAN catturato in Wireshark:

<p align="center">
    <img src="captures/vxlan_packet_details.png" width="600">
</p>

Analisi dell'intestazione VXLAN:

<p align="center">
    <img src="captures/vxlan_header_analysis.png" width="600">
</p>

---

## 👥 Contributors

- **Zefkilis2002** - Sviluppatore principale

Se desideri contribuire, puoi aprire una pull request o contattarmi direttamente! 🚀
