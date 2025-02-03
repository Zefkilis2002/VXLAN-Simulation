#!/usr/bin/env python

# Importazioni necessarie da Mininet e Python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import os

# Definizione della topologia VXLAN
class VXLANTopo(Topo):
    def __init__(self):
        super(VXLANTopo, self).__init__()

        # Creazione degli switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Creazione degli host
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        # Collegamento degli host agli switch
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(s1, s2)


def configure_vxlan(net):
    # Get switches
    s1, s2 = net.get('s1', 's2')
    
    # Configurazione degli indirizzi IP degli switch
    s1.cmd('ifconfig s1-eth2 192.168.1.1/24')
    s2.cmd('ifconfig s2-eth2 192.168.1.2/24')
    
    # Creazione delle interfacce VXLAN per incapsulare il traffico L2 in UDP/IP
    s1.cmd('ovs-vsctl add-port s1 vxlan1 -- set interface vxlan1 type=vxlan options:remote_ip=192.168.1.2 options:local_ip=192.168.1.1 options:key=1000')
    s2.cmd('ovs-vsctl add-port s2 vxlan2 -- set interface vxlan2 type=vxlan options:remote_ip=192.168.1.1 options:local_ip=192.168.1.2 options:key=1000')
    
    # Aggiunta di regole OpenFlow per inoltrare il traffico VXLAN
    s1.cmd('ovs-ofctl add-flow s1 "table=0,priority=100,in_port=1 actions=output:vxlan1"') # Inoltra pacchetti da h1 a vxlan1
    s1.cmd('ovs-ofctl add-flow s1 "table=0,priority=100,in_port=vxlan1 actions=output:1"') # Inoltra pacchetti VXLAN ricevuti a h1
    
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=100,in_port=1 actions=output:vxlan2"') # Inoltra pacchetti da h2 a vxlan2
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=100,in_port=vxlan2 actions=output:1"') # Inoltra pacchetti VXLAN ricevuti a h2

# Funzione per avviare la rete Mininet e applicare la configurazione
def start_network():
    # Creazione della topologia VXLAN definita in VXLANTopo
    topo = VXLANTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        controller=None,  # We'll use OpenFlow rules directly
        autoSetMacs=True
    )
    
    # Avviamo la rete virtuale
    net.start()
    
    # Configure VXLAN
    configure_vxlan(net)
    
    # Enable IP forwarding
    os.system('sysctl -w net.ipv4.ip_forward=1')
    
    print("*** Network started successfully")
    print("*** To test connectivity:")
    print("*** h1 ping h2")
    print("*** To check VXLAN encapsulation:")
    print("*** tcpdump -i any -nn port 4789")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_network()