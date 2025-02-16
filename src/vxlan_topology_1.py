#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
import os

class VXLANTopo(Topo):
    def __init__(self):
        super(VXLANTopo, self).__init__()

        # Creazione degli switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Creazione degli host
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        h3 = self.addHost('h3', ip='10.0.0.3/24')

        # Collegamento degli host agli switch
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s2)
        self.addLink(s1, s2)

def configure_vxlan(net):
    # Ottenere il riferimento agli switch
    s1, s2 = net.get('s1', 's2')
    
    # Configurazione degli indirizzi IP degli switch
    s1.cmd('ifconfig s1-eth2 192.168.1.1/24')
    s2.cmd('ifconfig s2-eth3 192.168.1.2/24')
    
    # Creazione delle interfacce VXLAN
    s1.cmd('ovs-vsctl add-port s1 vxlan1 -- set interface vxlan1 type=vxlan \
           options:remote_ip=192.168.1.2 options:local_ip=192.168.1.1 options:key=1000')
    s2.cmd('ovs-vsctl add-port s2 vxlan2 -- set interface vxlan2 type=vxlan \
           options:remote_ip=192.168.1.1 options:local_ip=192.168.1.2 options:key=1000')
    
    # Pulizia delle regole esistenti per evitare conflitti
    s1.cmd('ovs-ofctl del-flows s1')
    s2.cmd('ovs-ofctl del-flows s2')
    
    # Regole OpenFlow per s1
    # Il traffico in ingresso dalla porta 1 viene inoltrato alla porta 3 (tunnel VXLAN)
    s1.cmd('ovs-ofctl add-flow s1 "table=0,priority=1,in_port=1 actions=output:3"')
    # Il traffico in ingresso dalla porta 3 (tunnel VXLAN) viene inoltrato alla porta 1
    s1.cmd('ovs-ofctl add-flow s1 "table=0,priority=1,in_port=3 actions=output:1"')
    
    # Regole OpenFlow per s2
    # Il traffico locale tra h2 e h3 ha priorità più alta (priority=2)
    # Se il traffico arriva alla porta 1 ed è destinato a h3 (MAC 00:00:00:00:00:03), invialo alla porta 2
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=2,in_port=1,dl_dst=00:00:00:00:00:03 actions=output:2"')
    # Se il traffico arriva alla porta 2 ed è destinato a h2 (MAC 00:00:00:00:00:02), invialo alla porta 1
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=2,in_port=2,dl_dst=00:00:00:00:00:02 actions=output:1"')

    # Gestione del traffico verso h1
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=1,in_port=1,dl_dst=00:00:00:00:00:01 actions=output:4"')
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=1,in_port=2,dl_dst=00:00:00:00:00:01 actions=output:4"')

    # Gestione broadcast e traffico sconosciuto
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=1,dl_dst=ff:ff:ff:ff:ff:ff actions=ALL"')
    s2.cmd('ovs-ofctl add-flow s2 "table=0,priority=1 actions=NORMAL"')


def start_network():
    topo = VXLANTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        controller=None,
        autoSetMacs=True
    )
    
    net.start()
    
    # Configurazione VXLAN
    configure_vxlan(net)
    
    # Abilita l'inoltro IP
    os.system('sysctl -w net.ipv4.ip_forward=1')
    
    print("*** Network started successfully")
    print("*** To test connectivity:")
    print("*** h1 ping h2")
    print("*** h1 ping h3")
    print("*** h2 ping h3")
    print("*** To check VXLAN encapsulation:")
    print("*** tcpdump -i any -nn port 4789 or open Wireshark with udp.port == 4789")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_network()
